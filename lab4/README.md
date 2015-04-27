# Lab 4: Create and run a blueprint

The purpose of this lab is to fix a broken blueprint, install it locally and also upload it a Cloudify manager.

It is assumed that the exercise's files are extracted into `LAB_ROOT`.

### Step 1: Replace the placeholder

You need to replace **_all_** the occurrences of the placeholders (“`REPLACE_THIS_WITH`”) in **_all_** files, with the suitable values and to add missing parts as well.

Hint: Start with `tomcat-blueprint.yaml` and then fix the broken shell scripts.
There are placeholders in `tomcat-blueprint.yaml`, in some of the shell scripts and in the `tomcat.yaml` and `tomcat-local.yaml` files.

### Step 2: Run in local mode

Once you're done, you can run it in local mode:

```bash
cd ~work
cfy local init -p $LAB_ROOT/hello-tomcat/tomcat-blueprint.yaml -i $LAB_ROOT/hello-tomcat/tomcat-local.yaml
cfy local execute -w install
```

Now Browse to `http://127.0.0.1:8080/helloworld` (from the box itself, or `http://192.168.33.10:8080/helloworld` from the host) and then run the following CLI command:

```bash
cfy local outputs
```

To clean up:

```bash
cfy local execute -w uninstall
```

### Step 3: Existing manager

Upload the blueprint to the existing Cloudify manager, created in previous labs:

```bash
cd ~/work
cfy blueprints upload -p $LAB_ROOT/hello-tomcat/tomcat-blueprint.yaml -b hellotomcat
cfy deployments create -b hellotomcat -d hellotomcat -i $LAB_ROOT/hello-tomcat/tomcat.yaml
cfy executions start -d hellotomcat -w install
```

To test, navigate to port 8080 of the public IP associated with the VM on which installation was made:

```
http://15.125.87.108:8080
```

### Step 4: Cleanup

In order to clean up, remove the deployment and its blueprint:

```bash
cfy executions start -d hellotomcat -w uninstall
cfy deployments delete -d hellotomcat
cfy blueprints delete -b hellotomcat
```