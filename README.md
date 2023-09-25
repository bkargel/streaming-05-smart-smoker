# streaming-05-smart-smoker

> Use RabbitMQ to distribute tasks to multiple workers

One process will create task messages. Multiple worker processes will share the work. 


## Before You Begin

1. Fork this starter repo into your GitHub.
1. Clone your repo down to your machine.
1. View / Command Palette - then Python: Select Interpreter
1. Select your conda environment. 

## Description of the producer

The producer will read each row of the smoker-temps.csv file and send messages to three different queues. The message that each queue receives is based on the column in which the information is contained within the csv file. The smoker temp, FoodA temp, and FoodB temp, along with the timestamp are sent to their respective queues, with the producer reading one row every 30 seconds.

## RabbitMQ Admin 

Change show_offer to True in order to open the admin panel. When show_offer is false, the admin page will not open.

(Python makes it easy to open a web page - see the code to learn how.)

## Execute the Producer

1. Run bbq_producer.py 





## Reference

- [RabbitMQ Tutorial - Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)


## Screenshot

See a running example with at least 3 concurrent process windows here:

![Alt text](https://github.com/bkargel/streaming-05-smart-smoker/blob/main/Message_to_queues.png?raw=true "Sending to 3 queues")

## NOTES

It is always easier to change the name of a queue or change a message when it is contained within a variable. That way, you can just change the variable one time and it flows through the entire scipt, no matter how many times it is used within the code. 