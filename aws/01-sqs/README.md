# Objectives

1. Create an SQS queue
2. Submit messages to the queue
3. Receive messages from the queue
4. Delete the queue

# Prerequisites

1. Create an AWS account
2. Install the AWS CLI and configure it using `aws configure`
3. Install `boto3` using `python -m pip install boto3` or similar

# Running the test

In one console window, run `producer.py`.

The producer will create an SQS queue and write its URL to a text file.
It will then begin a random number of messages each second.

At any time, press `CTRL+C` to stop the producer.
It will automatically delete the text file and delete the SQS queue.

In another console window, run `consumer.py`.

The consumer will wait for the producer to write the queue URL to a text file.
When the URL is available the consumer will connect and begin receiving messages.

The consumer will try to receive up to 10 messages per request, and will wait up to 20 seconds.
This decreases I/O with AWS.

# Ending the test

Press `CTRL+C` to stop the producer.
It will wait 10 seconds, then clean up everything.

If the consumer is running it will automatically exit when the producer deletes the queue URL text file.
