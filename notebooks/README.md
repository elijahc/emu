# Basics

## THE EMU PIPELINE

![](https://animals.sandiegozoo.org/sites/default/files/inline-images/emu_face.jpg)

The emu data processing pipeline is built on top of [luigi](https://luigi.readthedocs.io/en/stable/) a flexible platform for building automating data processing jobs developed and maintained by spotify.

Luigi provides a framework takes define "tasks" within python classes and I've implemented a few for the processing pipeline. I found luigi really hard to wrap my head around at first so I decided to write up a quick primer to help make sense of it.

### How luigi does work for you

Luigi is decentralized, which means when you want
a job done you submit it to a job queue where it's
eventually executed in a separate "worker" process.
These don't exist on the same threads as the process
submitting the task by design. This means when you 
submit a task you can't the send variables with it.
Instead you supply filepath strings to data on disk
that the worker will load if necessary.

### Task Minimum Requirements

A luigi task is defined in a python class and
is deceptively simple. A fully functional
task only requires that you implement 2 methods:

1) An `output()` method (so it can check if its work has already been done)

2) A `run()` method which should perform your task and save the result in a file

The worker uses `output()` to check if the task has already been completed, and if not, executes `run()` to create the file.


Luigi tasks often also implement extra helper methods/functions. Functions implemented inside a class (by indenting their definitions) are only available within the class itself. You also access them through the `self` variable (e.g. `self.output()`, `self.run()`, etc)

### Concrete Example

The [Raw](https://github.com/elijahc/emu/blob/ce61030b89f878633ef6a97b4a26478c6824b5f8/emu/pipeline/download.py#L84) class in the emu pipeline codebase is a great example to explain a luigi task.[Raw](https://github.com/elijahc/emu/blob/ce61030b89f878633ef6a97b4a26478c6824b5f8/emu/pipeline/download.py#L84) is a
class I've implemented to download raw data files from box. Raw's purpose is simple: given a box file_id, download that file locally to a specified directory. Parameters of a luigi task are usually defined at the top of the class and Raw expects to receive:

- a box file_id of the file you want to download
- file_name (the name you want to save it as)
- save_to (the directory to save the file in)

When imported, luigi automagically makes these parameters available in the variable `self`. You access them by calling `self.file_id`, `self.file_name`, and `self.save_to` etc.

```python
class Raw(luigi.Task):
    # Task Parameters
    file_id = luigi.IntParameter() #Int
    file_name = luigi.Parameter() # filename
    save_to = luigi.Parameter() # Directory to save in

    # Helper method which does all the work
    def download(self):
        client = jwt()
        file = client.file(self.file_id)
        fp = os.path.join(self.out_dir(),self.file_name)

        with open(fp, 'wb') as open_file:
            file.download_to(open_file)
            open_file.close()

    # Implement your task in run
    def run(self):
        # ...
        # Download the file
        self.download()

    # Define where the output will end up
    def output(self):
        out_fp = os.path.join(self.out_dir(),self.file_name)
        return luigi.LocalTarget(out_fp)

```

We take advantage of inheritance in [BehaviorRaw](https://github.com/elijahc/emu/blob/ce61030b89f878633ef6a97b4a26478c6824b5f8/emu/pipeline/download.py#L122)
and [NLXRaw](https://github.com/elijahc/emu/blob/ce61030b89f878633ef6a97b4a26478c6824b5f8/emu/pipeline/download.py#L132) which both subclass Raw. [BehaviorRaw](https://github.com/elijahc/emu/blob/ce61030b89f878633ef6a97b4a26478c6824b5f8/emu/pipeline/download.py#L122) and [NLXRaw](https://github.com/elijahc/emu/blob/ce61030b89f878633ef6a97b4a26478c6824b5f8/emu/pipeline/download.py#L132) inherit/reuse Raw's `output()` and `run()` methods and so they they exist automatically 
without needed to define them again.

Similar classes can all inherit from a common base class to share common parameters or functions/methods. You can overwrite inherited methods by simply redefining them int he subclass. Because Behavior files and NLX files are saved in different folders we implement new `output_dir()` helper methods to direct them to be saved somewhere else when called by the 
original inherited `output()` method defined in Raw.

### Chaining the tasks together

The real power of a processing pipeline is the 
ability to chain tasks together and automate them. 
We can do this in luigi by making the output of a 
task contingent on completion of another task. 
A task specifies which other tasks it depends on in 
the optional `requires()` method. Raw and its derivatives 
don't depend on any other tasks to be executed, so 
they don't implement a `requires()`.