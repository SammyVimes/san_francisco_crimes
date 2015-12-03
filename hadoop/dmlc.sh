#!/bin/bash
if [ "$#" -lt 3 ];
then
	echo "Usage: <nworkers> <nthreads> <path_in_HDFS>"
	exit -1
fi

# кладём дату в HDFS
hadoop fs -mkdir $3/data
hadoop fs -put ../data/clean_train.txt.train $3/data
hadoop fs -put ../data/clean_train.txt.test $3/data

# TODO: не забыть вынести путь до DMLC в переменную (или вычислять)
# запускаем rabit, передавая адрес в hdfs
../../dmlc-core/tracker/dmlc_yarn.py  -n $1 --vcores $2 ../../xgboost.dmlc sf-crimes.conf nthread=$2\
    data=hdfs://$3/data/clean_train.txt.train\
    eval[test]=hdfs://$3/data/clean_train.txt.test\
    model_out=hdfs://$3/sf-crimes.final.model

# получаем модель
hadoop fs -get $3/sf-crimes.final.model final.model

# TODO: запускать wormhole_configurer

# выводим предикшн, таск в конфиге (TODO: эхо таска)
../../repo/dmlc-core/yarn/run_hdfs_prog.py ../../bin/xgboost.dmlc sf-crimes.conf task=pred model_in=final.model test:data=../data/clean_train.txt.test
# дампим бустеры модели final.model в dump.raw.txt
../../repo/dmlc-core/yarn/run_hdfs_prog.py ../../bin/xgboost.dmlc sf-crimes.conf task=dump model_in=final.model name_dump=dump.raw.txt
# визуализируем фичи
../../repo/dmlc-core/yarn/run_hdfs_prog.py ../../bin/xgboost.dmlc sf-crimes.conf task=dump model_in=final.model fmap=../data/featmap.txt name_dump=dump.nice.txt
#тада!
cat dump.nice.txt