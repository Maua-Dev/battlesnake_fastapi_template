import os
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    CfnOutput,
)
from constructs import Construct
from aws_cdk.aws_cloudwatch import ComparisonOperator
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_cloudwatch_actions import SnsAction


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.project_name = os.environ.get("PROJECT_NAME")
        self.aws_account_id = os.environ.get("AWS_ACCOUNT_ID_DEV")
        self.repo_slug = (
            os.environ.get("REPO_SLUG")
            or (os.environ.get("REPO_NAME") or "unknown").replace("_", "-")
        )

        lambda_role = iam.Role(
            self,
            "BattleSnakeLambdaRole",
            role_name=f"battlesnake-{self.repo_slug}-role-dev",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
            permissions_boundary=iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "PermissionsBoundary",
                f"arn:aws:iam::{self.aws_account_id}:policy/pb-battlesnake-participant",
            ),
        )

        lambda_fn = _lambda.Function(
            self,
            "BattleSnakeLambda",
            function_name=f"battlesnake-{self.repo_slug}-lambda-dev",
            runtime=_lambda.Runtime.PYTHON_3_13,
            code=_lambda.Code.from_asset("../src"),
            handler="app.main.handler",
            timeout=Duration.seconds(15),
            role=lambda_role,
        )

        lambda_url = lambda_fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
        )

        alarm = lambda_fn.metric_invocations(
            period=Duration.hours(6),
        ).create_alarm(
            self,
            "BattleSnakeLambdaAlarm",
            alarm_name=f"battlesnake-{self.repo_slug}-alarm-dev",
            threshold=5000,
            evaluation_periods=1,
            comparison_operator=ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
        )
        topic = Topic.from_topic_arn(
            self,
            self.project_name + "Topic",
            f"arn:aws:sns:{self.region}:{self.aws_account_id}:sns-battlesnake",
        )
        sns_action = SnsAction(topic)

        alarm.add_alarm_action(sns_action)

        CfnOutput(
            self,
            self.project_name + "Url",
            value=lambda_url.url,
            export_name=self.project_name + "UrlValue",
        )
