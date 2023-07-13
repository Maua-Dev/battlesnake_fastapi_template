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
from aws_cdk.aws_cloudwatch import ComparisonOperator
from aws_cdk.aws_sns import Topic

from aws_cdk.aws_cloudwatch_actions import SnsAction


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.project_name = os.environ.get("PROJECT_NAME")
        self.aws_account_id = os.environ.get("AWS_ACCOUNT_ID")

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

        
        alarm = lambda_fn.metric_invocations(
            period=Duration.hours(6),
        ).create_alarm(
            self, self.project_name +"LambdaAlarm",
            threshold=5000,
            evaluation_periods=1,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
        ) 
        topic = Topic.from_topic_arn(self, self.project_name + "Topic", f"arn:aws:sns:{self.region}:{self.aws_account_id}:sns-battlesnake")
        sns_action = SnsAction(topic)

        alarm.add_alarm_action(sns_action)

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
        

