import aws_cdk as core
import aws_cdk.assertions as assertions

from assignment03_cdk.assignment03_cdk_stack import Assignment03CdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in assignment03_cdk/assignment03_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Assignment03CdkStack(app, "assignment03-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
