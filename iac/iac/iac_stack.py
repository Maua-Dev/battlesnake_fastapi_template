import os
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    CfnOutput
)
from constructs import Construct

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        project_name = os.environ.get("PROJECT_NAME")

        lambda_fn = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset("../src"),
            handler="app.main.handler",
        )

        lambda_url = lambda_fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )

        CfnOutput(self, project_name + "Url",
                  value=lambda_url.url,
                  export_name= project_name + 'UrlValue')        
        

