import logging
import time

import boto3
import botocore.exceptions

import producer

log = logging.getLogger(__name__)
sqs = boto3.resource('sqs')


CALL_COUNT = 0
MESSAGE_COUNT = 0


def get_messages(queue):
    """Get messages, but track the number of invocations."""

    global CALL_COUNT, MESSAGE_COUNT
    CALL_COUNT += 1

    messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
    if messages:
        log.info(f"Received {len(messages)} messages")
        MESSAGE_COUNT += len(messages)
        queue.delete_messages(
            Entries=[
                {"Id": m.message_id, "ReceiptHandle": m.receipt_handle}
                for m in messages
            ]
        )
    return messages


def consume():
    """Connect to a queue and consume its messages."""

    log.info("Waiting for the queue to be created")
    log.info("(Press CTRL+C to exit immediately)")
    try:
        while not producer.URL_FILENAME.exists():
            time.sleep(10)
    except KeyboardInterrupt:
        log.info("Goodbye")
        return

    log.info("The queue should exist now")

    try:
        queue = sqs.Queue(producer.URL_FILENAME.read_text())
    except botocore.exceptions.ClientError as error:
        log.error("Unable to connect to queue: " + str(error))
        return

    try:
        while producer.URL_FILENAME.exists():
            get_messages(queue)
    except KeyboardInterrupt:
        pass

    log.info(f"{MESSAGE_COUNT} messages were retrieved")
    log.info(f"{CALL_COUNT} calls were made")
    log.info(f"Goodbye")


if __name__ == '__main__':
    consume()
