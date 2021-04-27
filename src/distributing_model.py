from pyspark.sql import SparkSession
from tensorflowonspark import TFCluster, TFNode

spark = SparkSession \
        .builder \
        .config("...")
        .appName("model-training") \
        .getOrCreate()
    spark.sparkContext.addPyFile("/usr/local/tensorflow/tfspark-{version}.zip")

cluster = TFCluster.run(spark.sparkContext,\
                        map_fun,\
                        args, \
                        num_executors=num_executors, \
                        num_ps=num_ps,\
                        tensorboard=False,\
                        driver_ps_nodes=False,\
                        input_mode=TFCluster.InputMode.SPARK)

if mode == "train":
        cluster.train(dataRDD, epochs)
    else:
        labelRDD = cluster.inference(dataRDD)


def map_fun(args, ctx):
    worker_num = ctx.worker_num
    job_name = ctx.job_name
    task_index = ctx.task_index  
    cluster, server = ctx.start_cluster_server(1)
    if job_name == "ps":
        server.join()     
    elif job_name == "worker":
        is_chiefing = (task_index == 0)
        with tf.device(tf.train.replica_device_setter(
                worker_device="/job:worker/task:%d" % task_index,
                cluster=cluster)):

            def build_model():
                pass

        hooks=[...]

        with tf.train.MonitoredTrainingSession(master=server.target,\
                                                is_chief=is_chiefing,
                                                checkpoint_dir=arsg['save_dir'],\
                                                hooks=hooks,\
                                                save_checkpoint_secs=600.)  as mon_sess:
            tf_feed = ctx.get_data_feed(train_mode=True)

            while not mon_sess.should_stop() and not tf_feed.should_stop():
                batch_data = tf_feed.next_batch(args['batch_size']))
                #apply what you need to be done here
                _ = mon_sess.run(...)

            if mon_sess.should_stop():
                tf_feed.terminate()
                    

with tf.device(tf.train.replica_device_setter(
                    worker_device="/job:worker/task:%d" % task_index,
                    cluster=cluster)):

    def build_model():
        model_input = tf.placeholder(tf.float32,\
                    [None,args['num_features'] ])
        model_labels = tf.placeholder(tf.float32, [None, args['num_classes']    ])
        logits = tf.keras.layers.Dense(args['num_classes'])(model_input)
        model_output = tf.nn.softmax(logits)

        tf_global_step = tf.train.get_or_create_global_step()
        tf_loss = tf.reduce_mean(tf.nn.weighted_cross_entropy_with_logits(logits=logits, targets=model_labels,pos_weight=weights))
        tf_optimizer = tf.train.AdamOptimizer(learning_rate=args['learning_rate']).minimize(tf_loss,
                                                                            global_step=tf.train.get_global_step())

    model_input,\
    model_labels,\
    model_output,\
    tf_global_step,\
    tf_loss,\
    tf_optimizer,\
    tf_metrics = build_model()

 with tf.train.MonitoredTrainingSession(master=server.target,\
                                                    is_chief=is_chiefing,
                                                    checkpoint_dir=arsg['save_dir'],\
                                                    hooks=hooks,\
                                                    save_checkpoint_secs=600.)  as mon_sess:
    tf_feed = ctx.get_data_feed(train_mode=True)

    step = 0
    while not mon_sess.should_stop() and not tf_feed.should_stop() and step < args['steps']:
        batch_data, batch_labels = get_next_batch(tf_feed.next_batch(args['batch_size']))

        if len(batch_data) > 0:
            feed = {model_input: batch_data, model_labels: batch_labels}
            _, logloss, step =  mon_sess.run([tf_optimizer, tf_loss,tf_global_step],feed_dict=feed)

    if mon_sess.should_stop() or step >= args['steps']:
        tf_feed.terminate()