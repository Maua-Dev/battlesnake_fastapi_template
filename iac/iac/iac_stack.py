import os
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    CfnOutput, 
    aws_iam as iam
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

        user = iam.User(self, project_name + "User",
                        user_name=project_name + "User",
                        password_reset_required=True,
                        password=project_name + "UserPassword"
                        )

        policy = iam.Policy(self, "Policy", statements=[
            iam.PolicyStatement(
                actions=["lambda:*"],
                resources=[lambda_fn.function_arn]
            )
        ])

        policy.add_statements(
            iam.PolicyStatement(
                actions=["logs:*"],
                resources=["arn:aws:logs:*:*:*"]
            )
        )

        policy.attach_to_user(user)


        CfnOutput(self, project_name + "Url",
                  value=lambda_url.url,
                  export_name= project_name + 'UrlValue')    

        CfnOutput(self, project_name + "User",
                  value=user.user_name,
                  export_name= project_name + 'UserValue'
                  )

        CfnOutput(self, project_name + "UserPassword",
                  value=user.user_name,
                  export_name= project_name + 'UserPasswordValue'
                  )    
        

