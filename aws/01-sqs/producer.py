import json
import logging
import pathlib
import random
import time

import boto3
import botocore.exceptions

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)
sqs = boto3.resource('sqs')


URL_FILENAME: pathlib.Path = pathlib.Path("QUEUE_URL.txt")


def produce():
    """Connect to a queue, then push messages to it at intervals."""

    message_count = 0

    try:
        queue = sqs.create_queue(
            QueueName=f"interact-with-queues-{random.randint(1000, 2000)}",
            Attributes={},
        )
    except botocore.exceptions.ClientError as error:
        log.error("Unable to create queue: " + str(error))
        return

    log.info(f"Queue available at '{queue.url}'")
    URL_FILENAME.write_text(queue.url)

    try:
        while True:
            messages = [
                {
                    "Id": str(i),
                    "MessageBody": json.dumps(
                        {
                            "created": str(int(time.time())),
                            "value": str(random.randint(0, 10)),
                        }
                    ),
                }
                for i in range(random.randint(1, 10))
            ]
            log.info(f"Submitting {len(messages)} messages")
            time.sleep(1)
            try:
                queue.send_messages(Entries=messages)
            except botocore.exceptions.ClientError as error:
                log.error("Unable to submit all messages: " + str(error))
                break
            message_count += len(messages)
    except KeyboardInterrupt:
        pass
    except Exception:
        log.exception("There was an error")
    finally:
        log.info("Cleaning up in 10 seconds")
        time.sleep(10)
        queue.delete()
        URL_FILENAME.unlink()

    log.info(f"Submitted {message_count} messages")


if __name__ == '__main__':
    produce()
