# Rebuild from nothing

The test of whether production is really described by your repository and your secrets manager.

## When

Once before launch, then yearly, and after a large change to hosting.

## Steps

1. In a scratch account or network, create the infrastructure from your written steps or scripts, not from memory.
2. Build the environment files from the secrets manager (scratch copies of the secrets).
3. Deploy the current signed artefact by digest. Verify its signature.
4. Restore the latest backup into the scratch database. Do not use production data outside production: use the restore-test method.
5. Run the smoke tests.
6. Time every step and write down anything you had to remember rather than read.
7. Delete the scratch environment and record that it is gone.

## Passed when

Someone who did not build production can follow the steps and reach a working system, and every gap you found is now written down.
