# PULUMI

## Install pulumi
```
curl -fsSL https://get.pulumi.com | sh
```
Check version
```
pulumi version
```

## Commands
### Create the infrastructure
```
pulumi up
```

### Add environment variables
```
pulumi config set {variable_name} {value}
```
This command will create a file Pulumi.dev.yaml with all environment variables.

### Destroy infrastructure
Remove all of the resources
```
pulumi destroy
```

If you want to destroy all history and configuration associated
```
pulumi stack rm dev
```

### Stack
Create a new stack, and active the stack
```
pulumi stack init stackName
```
List the stacks
```
pulumi stack ls
```
Change the active stack
```
pulumi stack select stackName
```
Use the outputs of the stack
```
pulumi stack output keyName
```
Example use the output stack in command line
```
curl $(pulumi stack output url)
```