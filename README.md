### aiplatgo

A [convince wrapper](#examples) for:

- [`gcloud ai-platform jobs submit training`](#train)
- [`gcloud ai-platform jobs submit prediction`](#pred)
- [`gcloud ai-platform local`](#local)

Because ...

["For convenience, it's useful to define your configuration values as environment variables.](https://cloud.google.com/ai-platform/training/docs/packaging-trainer#using_gcloud_to_package_and_upload_your_application_recommended) ... [Even if you use a YAML file, certain details must be supplied as command-line flags."](https://cloud.google.com/ai-platform/training/docs/training-jobs#formatting-your-configuration-parameters)

is silly.

--- 

`aiplatgo`'s config file to replaces the combination of CLI-flags and config file natively offered by [`gcloud ai platform`](https://cloud.google.com/sdk/gcloud/reference/ai-platform/). Moreover:

- The config file can contain all possible flags for training or prediction local or platform. Only relevant flags will be submitted .
- There are configurations to automatically handle naming conventions
- platform job directories can automatically be prefixed with `gs://bucket/folder`
- Underscores are accepted: ie `arg_name` for `arg-name`
- There are additional aliases for some args

---

<a name="examples">

### MINIMAL EXAMPLES

```yaml
# filename: config.yaml`
config:
    version: 1
    bucket: dev-ai-platform
    folder: gcs/folder/dev

args:
  package: trainer
  module: trainer.task
  region: us-central1

user:
    user_arg_1: 1
    user_arg_2: 2
```

The examples below assume the above config file is named `config.yaml`, and use the `--echo`-flag which prints out the command without executing:

```bash
# local train
aiplatgo local train config --echo
```

```bash
# output
gcloud ai-platform local train --package-path trainer --module-name trainer.task --user_arg_1 1 --user_arg_2 2 --job-dir v1/output
```

```bash
# platform training
aiplatgo train my_job config --echo
```

```bash
# output
gcloud ai-platform jobs submit training my_job --package-path trainer --module-name trainer.task --region us-central1 --user_arg_1 1 --user_arg_2 2 --job-dir gs://dev-ai-platform/gcs/folder/dev/my_job/v1/output --staging-bucket gs://dev-ai-platform/gcs/folder/dev/my_job/v1/staging
```

With command-line args/kwargs:

```bash
aiplatgo local train config distributed version=1234 worker-count=4 --echo
```

```bash
# output
gcloud ai-platform local train --distributed --package-path trainer --module-name trainer.task --worker-count 4 --user_arg_1 1 --user_arg_2 2 --job-dir v1/output
```

Adding a default_job_name:


```yaml
# filename: config.yaml`
config:
    name: my_default_job_name
    ...
```

```bash
aiplatgo train . config --echo
```

```bash
# output
gcloud ai-platform jobs submit training my_default_job_name --package-path trainer --module-name trainer.task --region us-central1 --user_arg_1 1 --user_arg_2 2 --job-dir gs://dev-ai-platform/gcs/folder/dev/my_default_job_name/v1/output --staging-bucket gs://dev-ai-platform/gcs/folder/dev/my_default_job_name/v1/staging
```

Note: similarly you can use `.` to skip a config file, only using command-line args/kwargs but at that point you should just go back to using Google's native `ai platform` CLI.

---

<a name='train'>

```bash
aiplatgo train --help
Usage: aiplatgo train [OPTIONS] NAME [CONFIG]

  submit prediction job to platform:  
    * name<optional>: job name. default or "." to use name from yaml([config][name])  
    * config<optional>: yaml config. default or "." uses kwargs only
    * additional args become flags <ie> "arg_name" => "--arg_name"
    * additional kwargs become kw-flags <ie> "arg_name=123" => "--arg_name 123"

Options:
  --echo BOOLEAN  if true print command without executing
  --help          Show this message and exit.
```

<a name='pred'>

```bash
aiplatgo predict --help
Usage: aiplatgo predict [OPTIONS] NAME [CONFIG]

  submit prediction job to platform:  
    * name<optional>: job name. default or "." to use name from yaml([config][name])  
    * config<optional>: yaml config. default or "." uses kwargs only
    * additional args become flags <ie> "arg_name" => "--arg_name"
    * additional kwargs become kw-flags <ie> "arg_name=123" => "--arg_name 123"

Options:
  --echo BOOLEAN  if true print command without executing
  --help          Show this message and exit.
```

<a name='local'>

```bash
aiplatgo local --help
Usage: aiplatgo local [OPTIONS] VERB [CONFIG]

  run local training or prediction:  
    * verb: "train" or "predict"  
    * config<optional>: yaml config. default or "." uses kwargs only
    * additional args become flags <ie> "arg_name" => "--arg_name"
    * additional kwargs become kw-flags <ie> "arg_name=123" => "--arg_name 123"

Options:
  --echo BOOLEAN  if true print command without executing
  --help          Show this message and exit.
```
