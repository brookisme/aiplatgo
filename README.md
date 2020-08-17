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
# aiplatgo config for auto-naming conventions, gs-bucket-info, etc...
config:
    version: 1
    bucket: dev-ai-platform
    folder: gcs/folder/dev


# google ai platform flags with values (ie --module-name MODULE_NAME )
args:
  package: trainer
  module: trainer.task
  region: us-central1


# google ai platform flags without values (ie --stream-logs )
flags:
  - distributed
  - stream-logs


# user-args
user:
    user_arg_1: 1
    user_arg_2: 2


# local-user-args (only added with `aiplatgo local ...`)
local:
    local_user_arg_1: 1
    local_user_arg_2: 2

# job-user-args (only added with `aiplatgo <train|predict> ...`)
job:
    local_user_arg_1: 1
    local_user_arg_2: 2
```

The examples below assume the above config file is named `config.yaml`, and use the `--echo/-e`-flag which prints out the command without executing:

```bash
# local train
aiplatgo local train config --echo
```

```bash
# output
gcloud ai-platform local train --package-path trainer --module-name trainer.task --job-dir v1/output --distributed --  --user_arg_1 1 --user_arg_2 2
```

```bash
# platform training (recommended: see below to specify job-name in config file)
aiplatgo train --name my_job config --echo
```

```bash
# output
gcloud ai-platform jobs submit training my_job --package-path trainer --module-name trainer.task --region us-central1 --job-dir gs://dev-ai-platform/output --staging-bucket gs://dev-ai-platform --stream-logs --  --user_arg_1 1 --user_arg_2 2
```

With command-line args/kwargs:

- `key=value` updates the `args` will update the `args` config, while `(config|flags|user).key=value` will update the `config/flags/user` config.  
- `flag_name`, ie word not followed by `=value`, becomes a cli flag (ex `stream-logs` becomes `--stream-logs`)

```bash
aiplatgo local train config config.version=1234 worker-count=4 --echo
```

```bash
# output
gcloud ai-platform local train --package-path trainer --module-name trainer.task --worker-count 2 --job-dir my_default_job_name/v1234/output --distributed --  --user_arg_1 1 --user_arg_2 2
```

Adding a default_job_name:


```yaml
# filename: config.yaml`
config:
    name: my_default_job_name
    ...
```

```bash
aiplatgo train config --echo
```

```bash
# output
gcloud ai-platform jobs submit training my_default_job_name --package-path trainer --module-name trainer.task --region us-central1 --job-dir gs://dev-ai-platform/output --staging-bucket gs://dev-ai-platform --stream-logs --  --user_arg_1 1 --user_arg_2 2
```

Note: similarly you can use `.` to skip a config file, only using command-line args/kwargs but at that point you should just go back to using Google's native `ai platform` CLI.

---

<a name='train'>

```bash
aiplatgo train --help
Usage: aiplatgo train [OPTIONS] [CONFIG]

  submit training job to platform:  * config<optional>: yaml config. default
  or "." uses kwargs only  * additional args become flags <ie> "arg_name" =>
  "--arg_name"  * additional kwargs become kw-flags <ie> "arg_name=123" => "
  --arg_name 123"

Options:
  -n, --name TEXT  by default uses `config.name` for the job name. pass --name
                   to override

  -e, --echo       if true print command without executing
  -t, --timestamp  append timestamp (YYYYMMDD_HMS) to job name
  --help           Show this message and exit.
```

<a name='pred'>

```bash
aiplatgo predict --help
Usage: aiplatgo predict [OPTIONS] [CONFIG]

  submit prediction job to platform:  * config<optional>: yaml config.
  default or "." uses kwargs only  * additional args become flags <ie>
  "arg_name" => "--arg_name"  * additional kwargs become kw-flags <ie>
  "arg_name=123" => "--arg_name 123"

Options:
  -n, --name TEXT  by default uses `config.name` for the job name. pass --name
                   to override

  -e, --echo       if true print command without executing
  -t, --timestamp  append timestamp (YYYYMMDD_HMS) to job name
  --help           Show this message and exit.
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
