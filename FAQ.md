# How do I add external packages?
Add the names of the required packages in the _packages_ field in the ```.aws_lambda_mess.json``` file.

```json
{
    "source":  "src",
    "packages": [
        "aws_lambda_mess",
        "next_package",
        ...
    ]
}
```