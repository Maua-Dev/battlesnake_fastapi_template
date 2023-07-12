import os
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    CfnOutput, 
    aws_iam as iam,
    SecretValue
)
from constructs import Construct

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.project_name = os.environ.get("PROJECT_NAME")

        lambda_fn = _lambda.Function(
            self,
            "BattleSnakeLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("../src"),
            handler="app.main.handler",
            timeout=Duration.seconds(15),
        )

        lambda_url = lambda_fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )

        password = self.project_name + "UserPassword7@"

        user = iam.User(self, self.project_name + "User",
                        user_name=self.project_name + "User",
                        password_reset_required=True,
                        password=SecretValue.unsafe_plain_text(password)
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

        user.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("IAMUserChangePassword")
        )

        CfnOutput(self, self.project_name + "Url",
                  value=lambda_url.url,
                  export_name= self.project_name + 'UrlValue')    

        CfnOutput(self, self.project_name + "UserOutput",
                  value=user.user_name,
                  export_name= self.project_name + 'UserValue'
                  )

        CfnOutput(self, self.project_name + "FirstTimeUserPassword",
                  value=password,
                  export_name= self.project_name + 'FirstTimeUserPasswordValue'
                  )    
        
        CfnOutput(self, self.project_name + "LambdaConsole",
                    value="https://" + self.region + ".console.aws.amazon.com/lambda/home?region=" + self.region + "#/functions/" + lambda_fn.function_name + "?tab=code",
                    export_name= self.project_name + 'LambdaConsoleValue'
                    )
        

