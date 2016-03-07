/*
Implementation:
The farmer checks for, and processes, messages from the workers
Initially, it sets up the A to B interval as the first task in the bag
It reacts to requests for tasks by attempting to provide new tasks from the bag
It reacts to tasks being produced by adding the tasks to the bag
It reacts to workers returning results by adding the results to a running total
It tracks the number of active workers, incrementing the count when a task is given out, and decrementing it when a result or two tasks are returned.
When there are no more tasks, and all workers are inactive, it shuts down the workers and returns the final result

The workers check for, and process, messages from the farmer
If the farmer declares there are no tasks available, the worker polls the farmer until a task becomes available
If the farmer declares there will be no more tasks, the worker shuts down
If the farmer produces a task for the worker, the worker computes area, and then either sends a result or two new tasks to the farmer depending on the accuracy of the area computed

Choice of MPI primitives:
MPI_Send and MPI_Recv used to pass data between processes.
MPI_Send was used as it is the simplest send to use, from a programming perspective, and accomplishes what it needs to.
MPI_Recv was used for similar reasons.
MPI_Probe was used to check for messages to process, to allow the message to be handled properly. Again, the simplest option available.
Ready-mode versions of send/receive could have been used, but this would potentially have added complexity to the code, making it more difficult to produce/bug-fix. 
Immediate versions of send/receive/probe could have been used, but this would have required extra code, again, to ensure a correct implementation.
As speed etc. was not a requirement of the program, using the simplest available method was sufficient, and enabled faster development.
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include "stack.h"

#define EPSILON 1e-3
#define F(arg)  cosh(arg)*cosh(arg)*cosh(arg)*cosh(arg)
#define A 0.0
#define B 5.0

#define SLEEPTIME 1

// Messages from the workers
#define WORKER_GET_TASK 50 // request a new task
#define WORKER_ADD_TASKS 51 // add two new tasks to the bag
#define WORKER_RETURN_RESULT 52 // return the result if we meet the criteria
// Messages from the farmer
#define FARMER_TASK 53 // give the worker a task
#define FARMER_NO_TASK 54 // inform the worker that there is currently no task
#define FARMER_NO_MORE_TASKS 55 // inform the worker that there will be no further tasks

double dummy_data[2] = {0, 0};

int *tasks_per_process;

double farmer(int);

void worker(int);

int main(int argc, char **argv ) {
  int i, myid, numprocs; // numprocs passed in as a CLI argument
  double area, a, b;

  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
  MPI_Comm_rank(MPI_COMM_WORLD,&myid);

  if(numprocs < 2) {
    fprintf(stderr, "ERROR: Must have at least 2 processes to run\n");
    MPI_Finalize();
    exit(1);
  }

  if (myid == 0) { // Farmer
    // init counters
    tasks_per_process = (int *) malloc(sizeof(int)*(numprocs));
    for (i=0; i<numprocs; i++) {
      tasks_per_process[i]=0;
    }
  }

  if (myid == 0) { // Farmer
    area = farmer(numprocs);
  } else { //Workers
    worker(myid);
  }

  if(myid == 0) {
    fprintf(stdout, "Area=%lf\n", area);
    fprintf(stdout, "\nTasks Per Process\n");
    for (i=0; i<numprocs; i++) {
      fprintf(stdout, "%d\t", i);
    }
    fprintf(stdout, "\n");
    for (i=0; i<numprocs; i++) {
      fprintf(stdout, "%d\t", tasks_per_process[i]);
    }
    fprintf(stdout, "\n");
    free(tasks_per_process);
  }
  MPI_Finalize();
  return 0;
}

double farmer(int numprocs) {
  stack *stack = new_stack();
  double range[2] = {A, B};
  push(range, stack);
  
  int active_workers = 0;
  double final_result = 0;
  
  double rec_data[2];
  double rec_data_tasks[3];
  double rec_data_result[1];
  MPI_Status status;
  
  while(1) {
    if (is_empty(stack) && active_workers == 0) { // Computation has completed: cleanup and return result
      int i;
      for (i = 1; i < numprocs; ++i) {
        MPI_Send(dummy_data, 2, MPI_DOUBLE, i, FARMER_NO_MORE_TASKS, MPI_COMM_WORLD);
      }
      free_stack(stack);
      return final_result;
    }
    
    MPI_Probe(MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status); // Wait for a message
    
    if (status.MPI_TAG == WORKER_GET_TASK) { // Worker looking for a new task
      MPI_Recv(rec_data, 2, MPI_DOUBLE, MPI_ANY_SOURCE, WORKER_GET_TASK, MPI_COMM_WORLD, &status);
      
      if (is_empty(stack)) { // If there are no tasks remaining, inform the worker
        MPI_Send(dummy_data, 2, MPI_DOUBLE, status.MPI_SOURCE, FARMER_NO_TASK, MPI_COMM_WORLD);
      } else { // If there are tasks remaining, provide one to the worker
        double *snd_dat = pop(stack);
        MPI_Send(snd_dat, 2, MPI_DOUBLE, status.MPI_SOURCE, FARMER_TASK, MPI_COMM_WORLD);
        ++tasks_per_process[status.MPI_SOURCE]; // count number of tasks given to each worker
        ++active_workers;
      }
    } else if (status.MPI_TAG == WORKER_ADD_TASKS) { // Worker returning a pair of tasks, which get added to the bag
      MPI_Recv(rec_data_tasks, 3, MPI_DOUBLE, MPI_ANY_SOURCE, WORKER_ADD_TASKS, MPI_COMM_WORLD, &status);
      int i;
      for (i = 0; i < 2; ++i) {
        range[0] = rec_data_tasks[i];
        range[1] = rec_data_tasks[i+1];
        push(range, stack);
      }
      --active_workers;
    } else if (status.MPI_TAG == WORKER_RETURN_RESULT) { // Worker returning a result, which gets addes to the total
      MPI_Recv(rec_data_result, 1, MPI_DOUBLE, MPI_ANY_SOURCE, WORKER_RETURN_RESULT, MPI_COMM_WORLD, &status);
      final_result += rec_data_result[0];
      --active_workers;
    }
  }
}

void worker(int mypid) {
  double snd_data[3];
  double snd_data_result[1];
  double rec_data[2];
  double mid, fmid, larea, rarea, left, right, fleft, fright, lrarea;
  MPI_Status status;
  
  while(1) {
    // All sends/receives aimed at process 0, the farmer
    MPI_Send(dummy_data, 2, MPI_DOUBLE, 0, WORKER_GET_TASK, MPI_COMM_WORLD); // Attempt to get a task
    MPI_Recv(rec_data, 2, MPI_DOUBLE, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

    usleep(SLEEPTIME); // Allow multiprocess simulation
    
		if (status.MPI_TAG == FARMER_NO_TASK) { // No task currently - try again (with a delay/in a multiprocess manner due to 'usleep')
      continue; 
    } else if (status.MPI_TAG == FARMER_NO_MORE_TASKS) { // No more tasks - end the worker
      return; 
    }
    
    // Calculate area
    left = rec_data[0];
    right = rec_data[1];
    mid = (left + right) / 2;
    fleft = F(left);
    fmid = F(mid);
    fright = F(right);
    larea = (fleft + fmid) * (mid - left) / 2;
    rarea = (fmid + fright) * (right - mid) / 2;
    lrarea = (fleft + fright) * ((right - left)/2);
    
    if(fabs((larea + rarea) - lrarea) > EPSILON) { // Area not accurate enough - create 2 new tasks
      snd_data[0] = left;
      snd_data[1] = mid;
      snd_data[2] = right;
      MPI_Send(snd_data, 3, MPI_DOUBLE, 0, WORKER_ADD_TASKS, MPI_COMM_WORLD);
    } else { // Area accurate enough - send result
      snd_data_result[0] = larea + rarea;
      MPI_Send(snd_data_result, 1, MPI_DOUBLE, 0, WORKER_RETURN_RESULT, MPI_COMM_WORLD);
    }
  }
}
