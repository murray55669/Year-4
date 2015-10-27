for var1 in 0 1 2 3 4
do
    echo part-0000$var1
    hdfs dfs -cat /user/$USER/data/$1/part-0000$var1 | head 
done
