# Abaco

## Requirements

1. TACC Account: https://portal.tacc.utexas.edu/account-request
2. Create a Docker account: https://hub.docker.com/
3. Install the TACC Cloud Python SDK - ` pip3 install agavepy `

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


## Exercise: Deploy a hello-world container with Abaco

  Let's begin with a simple example of printing "hello-world" using an Abaco Actor. 

  For this example, create a new local directory to hold your work.

* A Basic Python File hello-world.py with a function to print the message (e.g: hello-world! ) sent to the actor when run. 

  ```
  # hello-world.py

  from agavepy.actors import get_context

  # function to print the message
  def echo_message(m):
      print(m)

  def main():
      context = get_context()
      message = context['raw_message']
      echo_message(message)

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
  docker build -t user/hello-world-actor . 

  docker push user/hello-world-actor  
  ```
  
  
* Register the Actor 

  Register the Docker image as an Abaco actor with the Agave client. 

  ```
  from agavepy.agave import Agave
  ag = Agave(api_server='https://api.tacc.utexas.edu', token='<access_token>')
  my_actor = {"image": "user/hello-world-actor", "name": "hello-world-actor", "description": "Simple actor to say hello-  
  world."}
  ag.actors.add(body=my_actor)
  ``` 
  
  > {'_links': {'executions': 'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq/executions', 'owner': 
  'https://api.tacc.utexas.edu/profiles/v2/sgopal', 'self': 'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq'}, 
  'createTime': '2019-11-04 16:50:49.155654', 'defaultEnvironment': {}, 'description': 'Simple actor to print hello-world.', 
  'gid': 862347, 'hints': [], 'id': 'RxbWwWyWpealq', 'image': 'reshg/hello-world-actor', 'lastUpdateTime': '2019-11-04 
  16:50:49.155654', 'link': '', 'mounts': [], 'name': 'hello-world-actor', 'owner': 'sgopal', 'privileged': False, 'queue': 
  'default', 'state': {}, 'stateless': True, 'status': 'SUBMITTED', 'statusMessage': '', 'tasdir': '06935/sgopal', 'token': 
  'false', 'type': 'none', 'uid': 862347, 'useContainerUid': False, 'webhook': ''}
  
  
  The output prints an **actor id** for the actor registered. 

* Check the status of the actor :

  ```
  ag.actors.get(actorId='actorId')
  ```

  > {'_links': {'executions': 'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq/executions', 'owner': 
  'https://api.tacc.utexas.edu/profiles/v2/sgopal', 'self': 'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq'}, 
  'createTime': '2019-11-04 16:50:49.155654', 'defaultEnvironment': {}, 'description': 'Simple actor to print hello-world.', 
  'gid': 862347, 'hints': [], 'id': 'RxbWwWyWpealq', 'image': 'reshg/hello-world-actor', 'lastUpdateTime': '2019-11-04 
  16:50:49.155654', 'link': '', 'mounts': [], 'name': 'hello-world-actor', 'owner': 'sgopal', 'privileged': False, 'queue': 
  'default', 'state': {}, 'stateless': True, 'status': 'READY', 'statusMessage': ' ', 'tasdir': '06935/sgopal', 'token': 
  'false', 'type': 'none', 'uid': 862347, 'useContainerUid': False, 'webhook': ''}
  
  When the actor's worker is initialized, it's **status** will change from SUBMITTED to READY. 

* Executing the Actor

  We can test the Actor:

  ``` 
  ag.actors.sendMessage(actorId='actorId',
                           body={'message': 'Actor, this is test!'})
  ag.actors.sendMessage(actorId='actorId', body={'message':'Hello-world!'})
  ```
  
  
  > {'_links': {'messages': 'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq/messages', 'owner': 
  'https://api.tacc.utexas.edu/profiles/v2/sgopal', 'self': 
  'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq/executions/zXpPjZmDVNDWr'}, 'executionId': 'zXpPjZmDVNDWr', 'msg': 
  'Hello-world!'}
  
  This started an execution for the actor and throws an **execution id**. 
  Once a message is sent to an actor, workers for the actor take the message and start an actor container with the message.  

  To get status of the execution, use the actor id and execution id:

  ``` 
  ag.actors.getExecution(actorId=actorId, executionId=executionId)
  ```
  
  > {'_links': {'logs': 'https://api.tacc.utexas.edu/actors/v2/TACC-PROD_RxbWwWyWpealq/executions/zXpPjZmDVNDWr/logs',  
  'owner': 'https://api.tacc.utexas.edu/profiles/v2/sgopal', 'self': 'https://api.tacc.utexas.edu/actors/v2/TACC-
   PROD_RxbWwWyWpealq/executions/zXpPjZmDVNDWr'}, 'actorId': 'RxbWwWyWpealq', 'apiServer': 'https://api.tacc.utexas.edu', 
   'cpu': 0, 'executor': 'sgopal', 'exitCode': 0, 'finalState': {'Dead': False, 'Error': '', 'ExitCode': 0, 'FinishedAt': 
   '2019-11-04T16:51:42.785892147Z', 'OOMKilled': False, 'Paused': False, 'Pid': 0, 'Restarting': False, 'Running': False, 
   'StartedAt': '2019-11-04T16:51:42.448167824Z', 'Status': 'exited'}, 'id': 'zXpPjZmDVNDWr', 'io': 0, 'messageReceivedTime': 
   '2019-11-04 16:51:31.502243', 'runtime': 1, 'startTime': '2019-11-04 16:51:41.754348', 'status': 'COMPLETE', 'workerId': 
   'oAG8X0lvEJ0rR'}

* View the logs

  Logs endpoint makes the standard out from an actor execution available for viewing. 

  ``` 
  ag.actors.getExecutionLogs(actorId=actorId, executionId=executionId)
  ```
  
  > {'_links': {'execution': 'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq/executions/zXpPjZmDVNDWr', 'owner': 
   'https://api.tacc.utexas.edu/profiles/v2/sgopal', 'self':  
   'https://api.tacc.utexas.edu/actors/v2/RxbWwWyWpealq/executions/zXpPjZmDVNDWr/logs'}, 'logs': 'Hello-world!\n'}


### With Abaco CLI

- The Abaco CLI is a command line toolkit for developing, managing and using Abaco Actors.

* Clone the repository and create authentication tokan as shown below to get started 

  ```
  git clone https://github.com/TACC-Cloud/abaco-cli.git 
  source abaco-cli/abaco-completion.sh
  export PATH=$PATH:$PWD/abaco-cli/
  auth-tokens-create -S
  ```

* There are multiple ~15 subcommands with the CLI. We can create, list, delete, update, submit, check logs etc with the abaco   CLI. 

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
