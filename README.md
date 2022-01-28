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
pulumi config ser {variable_name} {value}
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