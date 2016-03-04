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
// WORKER_GET_TASK - request a new task
#define WORKER_GET_TASK 50
// WORKER_ADD_TASKS - add two new tasks to the bad
#define WORKER_ADD_TASKS 51
// WORKER_RETURN_RESULT - return the result if we meet the criteria
#define WORKER_RETURN_RESULT 52
// Messages from the farmer
// FARMER_TASK - give the worker a task
#define FARMER_TASK 53
// FARMER_NO_TASK - inform the worker that there is currently no task
#define FARMER_NO_TASK 54
// FARMER_NO_MORE_TASKS - inform the worker that there will be no further tasks
#define FARMER_NO_MORE_TASKS 55

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
  // You must complete this function
  /*
    Use stack pre-implemented to store tasks?
    Store tasks as a stack of LPoint, RPoint pairs
    
    Initial: push {A,B} onto the stack
    
    Loop: probe the COMM channel for 
  */
}

void worker(int mypid) {
  // You must complete this function
  
  usleep(SLEEPTIME); // Allow multiprocess simulation
}
