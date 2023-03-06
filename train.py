def getImageFromPath(path):
    return os.path.basename(os.path.dirname(os.path.normpath(path)))


class TrainingThread(threading.Thread):
    def __init__(self, thread_id, path):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.path = path

    def run(self):
        print("Starting thread " + str(self.thread_id))
        data = turi.image_analysis.load_images(self.path, with_path=True)
        data["people"] = data["path"].apply(lambda path: getImageFromPath(path))
        train_data, test_data = data.random_split(0.8)
        model = turi.image_classifier.create(train_data, target='people', model='squeezenet_v1.1', verbose=True)
        metrics = model.evaluate(test_data)
        print("Thread " + str(self.thread_id) + " accuracy: " + str(metrics["accuracy"]))
        model.export_coreml(self.path + "/people.mlmodel")
        print("Thread " + str(self.thread_id) + " done.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python train.py <directory>")
        sys.exit(1)

    myPath = "uploads/" + sys.argv[1]

    if threading.active_count() == 1:
        # if the main thread is the only active thread, don't run concurrent threads
        print("Running in single-threaded mode.")
        data = turi.image_analysis.load_images(myPath, with_path=True)
        data["people"] = data["path"].apply(lambda path: getImageFromPath(path))
        train_data, test_data = data.random_split(0.8)
        model = turi.image_classifier.create(train_data, target='people', model='squeezenet_v1.1', verbose=True)
        metrics = model.evaluate(test_data)
        print("Accuracy: " + str(metrics["accuracy"]))
        model.export_coreml(myPath + "/people.mlmodel")
    else:
        # if there are active threads other than the main thread, run concurrent threads
        print("Running in multi-threaded mode.")
        threads = []
        for i in range(3):  # train 3 models concurrently
            thread = TrainingThread(i+1, myPath)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        print("All threads done.")