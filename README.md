# Abaco

## Requirements

1. TACC Account: https://portal.tacc.utexas.edu/account-request
2. Create a Docker account: https://hub.docker.com/
3. Install the TACC Cloud Python SDK

## Getting Started

### With Python-SDK

With the requirements in place, you are now ready to get started. 

* We need to create an OAuth Client:

  ```
  from agavepy.agave import Agave
  ag = Agave(api_server='https://api.tacc.utexas.edu',
  ...            username='your username',
  ...            password='your password')
  ag.clients.create(body={'clientName': 'enter a client name'})
  ```

  Save your consumerKey and consumerSecret. The OAuth client keys can be reused as well. 

* Once we have this in place, generate a Token: 

  ```
  ag.token.create()
  ```
  Grab the token generated and store it. 

  Running ` ag.profiles.get() ` would show the current user's profile. 


## Exercise: Deploy and test a hello-world container with Abaco

  Let's begin with a simple example of printing "hello-world" using an Abaco Actor. 

  For this example, create a new local directory to hold your work.

* A Basic Python File hello-world.py with a function to print the message (e.g: hello-world! ) sent to the actor when run. 

  ```
  # hello-world.py

  from agavepy.actors import get_context

  # function to print the message
  def say_hello(message):
     print(message)

  def main():
     context = get_context()
     message = context['raw_message']
     say_hello(message)

  if __name__ == '__main__':
     main()
  ``` 

* Within the same directory, create a Dockerfile to register the function as an Abaco actor. 

  ```
  FROM python:3.6

  # install agavepy
  RUN pip install --no-cache-dir agavepy
  
  # add the python script to docker container
  ADD hello.py /hello.py
  
  # command to run the python script
  CMD ["python", "/hello.py"]
  ```

  Build and push the docker image to Docker Hub. 
  
  ```
  docker build -t dockerhub_username/actorimagetag . 

  docker push dockerhub_username/actorimagetag  
  ```
  
  
* Register the Actor 
  Register the Docker image as an Abaco actor with the Agave client. 

  ```
  from agavepy.agave import Agave
  ag = Agave(api_server='https://api.tacc.utexas.edu', token='<access_token>')
  my_actor = {"image": "user/my_actor", "name": "hello-world-actor", "description": "Simple actor to say hello-world."}
  ag.actors.add(body=my_actor)
  ``` 
  
  <img src="inst/add_actor.png" height="50" width="75">
  
  The output prints an **actor id** for the actor registered. 

* Check the status of the actor :

  ```
  ag.actors.get(actorId='actorId')
  ```
  <img src="inst/actor_status.png" width="250">
  
  When the actor's worker is initialized, it's **status** will change from SUBMITTED to READY. 

* Executing the Actor

  We can test the Actor:

  ``` 
  ag.actors.sendMessage(actorId='actorId',
                           body={'message': 'Actor, this is test!'})
  ag.actors.sendMessage(actorId='actorId', body={'message':'Hello-world!'})
  ```
  
  
  <img src="inst/send_message.png" width="250">

  This started an execution for the actor and throws an **execution id**. 
  Once a message is sent to an actor, workers for the actor take the message and start an actor container with the message.  

  To get status of the execution, use the actor id and execution id:

  ``` 
  ag.actors.getExecution(actorId=actorId, executionId=executionId)
  ```
  
  <img src="inst/getExecution.png" width="250">

* View the logs

  Logs endpoint makes the standard out from an actor execution available for viewing. 

  ``` 
  ag.actors.getExecutionLogs(actorId=actorId, executionId=executionId)
  ```
  
  <img src="inst/execution_logs.png" width="250">



### With Abaco CLI

- The Abaco CLI is a command line toolkit for developing, managing and using Abaco Actors.

* Clone the repository and create authentication tokan as shown below to get started 

  ```
  git clone https://github.com/TACC-Cloud/abaco-cli.git 
  source abaco-cli/abaco-completion.sh
  export PATH=$PATH:$PWD/abaco-cli/
  auth-tokens-create -S
  ```

* There are multiple ~15 subcommands with the CLI. We can create, list, delete, update, submit, check logs etc with the abaco CLI. 

* Here, we illustrate how to list, send message, view logs, delete the actor we created with the SDK. 

  1.) List the abaco names
  
      ``` 
      abaco list  
      ```
     
      Returns list of actor names, IDs, and statuses (or the JSON description of
      an actor if an ID or alias is provided)
     
      > hello-world-actor  RxbWwWyWpealq  READY

  2.) Run the actor by sending a message
  
      ```
      abaco submit -m "hello-world" RxbWwWyWpealq
      ```
    
      Output:
      > R5jlv4RzKqQPe
        hello-world

      This prints the execution id.
      
  3.) Check execution/job status 
  
     ``` 
     abaco executions RxbWwWyWpealq R5jlv4RzKqQPe   
     ```
     
     > pvkBpWRXGXl4z  COMPLETE
     
  4.) Examine logs
     
     ```
     abaco logs RxbWwWyWpealq R5jlv4RzKqQPe   
     ```
     
     > Logs for execution R5jlv4RzKqQPe:
       hello-world
       
   5.) Sharing the actor
      Giving READ permissions to another user. 
      
      ```
      abaco permissions -u jfonner -p READ R5jlv4RzKqQPe   
      ```
   
   6.) Delete an actor
   
      ```
      abaco delete actorId    
      ```
      
      > Actor deleted successfully. 
