# Alexa, do my taxes

I think if Alexa could _actually_ do my taxes then Jeff Bezos would be the richest man on earth /s

This tutorial is a light introduction into getting a basic skill setup on Amazon Alexa, using AWS Lambda and CapitalOne's UK developer API.

## Prerequisites
Before we get started we need 2 accounts:
1. AWS Account - https://aws.amazon.com/Sign-Up‎
2. Amazon Developer Account - https://developer.amazon.com/

It should be pretty quick setting both of these things up, your AWS account may require card info but it won't charge your account unless you start using chargable resources. The material in this tutorial *DOES NOT* cause any charges to your account.

## Getting Started

### Setting up you Alexa Skill

After you've setup and logged into the https://developer.amazon.com/ console we can create a simple skill.

#### Creating a blank Skill
1. Click on "Your Alexa Consoles" -> "Skills"
2. Now "Create Skill"
3. Name your skill something appropraite for instance "banking app"
	a. Language - English(UK)
	b. Under the choose a model section, select - Custom (should be selected by default)
	c. When choosing a method to host your skills resources - Custom (should also be default)
	d. "Create Skill"
4. Choose a template - Start from scratch

Congrats, the skills created, although it's nothing more than a shell with a name that literally does nothing - lets give it a purpose (insert Rick & Morty robot joke [here](https://www.youtube.com/watch?v=X7HmltUWXgs))

#### Giving the Skill a purpose
1. Copy the contents of the model.json file found in this repo under the models folder, or click here *to-do link model*
2. On the left of your developer console go to the "JSON Editor" under "Interaction Model"
3. Paste the contents of the json file here and click "Save Model" at the top

Should everything have worked correctly you will now see 2 intents having appeared under your invocation model:
- GetAccountInfo
- ListPendingTransactions
These are the function calls you'll be passing into the backend service, and if you check out there sample utterances you'll see some sample phrases prepopulated that can be used on Alexa for calling this specific function - feel free to add more, just make them relevant.

We've got mose of our skill setup done now, so open a new tab and we'll move onto the backend functionality that's going to "do my taxes".

### Setting up your Lambda

Make sure you're logged into https://aws.amazon.com

#### Download the example Lambda
I've already created a sample Lambda which you'll be able to build on make go ahead and download it from the following link:
https://s3-eu-west-1.amazonaws.com/ryan109-workshop-storage/alexa-tutorial/lambda_function.zip

#### Creating your Lambda
1. Type "Lambda" into the aws search box
2. "Create Function"
3. "Author from scratch"
	a. Give your function a relevant name "alexa_banking_skill"
	b. Runtime -> Python 3.6
	c. Create Lambda
4. Scroll down to the "Function Code" section, under "Code entry type" choose "Upload a .zip file"
	a. Select the downloaded lambda zip
	b. Press "Save" at the top right
5. Save the updated function

#### Testing your Lambda
1. Configure a new test event using the drop down beside the test button
2. Copy getAccountInfo & getPendingTransactions json models saved in this repo, and create a test event for each one.
3. Press "test", on the log output you should get a response relevant to the event you're testing.

Note: The transaction test may time out from time to time, this is a problem with API it's trying to hit.

#### Adding an Alexa trigger to hit your Lambda
Now that our Lambda is working we need to plug it in to our Alexa skill so she can finally do our taxes, for this naviagte to the "deisinger" tab at the top of the page:
1. Click the Alexa skills kit from the left hand side, this should add it to your stack.
2. Click on "configuration required" under the newly added trigger
3. Swap tabs back over to your skill and click on the "Endpoint" section from the drop down on the left
	a. Select AWS Lambda
	b. Copy your skill ID
4. Swap back over to the Lambda console and paste your skill ID in the required box.
5. Now copy the ARN of your Lambda which you can find in the top right of your console e.g: arn:aws:lambda:eu-west-1:0000000000000:function:example_lambda
6. Swap back over to your skill and paste it in the "default region" box just under where Skill ID is noted.
7. Save both your Skill and your Lambda.

Now say the magic words and pray to whatever serpent God you believe in...geddit, Python? (Still have no idea why I chose programming over stand up)

It's time to start chatting up Alexa and see what she can do.

### Piecing the puzzle together

Go to your Alexa Skill and along the top click on the "testing" tab, then make sure the "Skill testing is enabled in" - Development.

On the left you'll see the Alexa simulator where you can have a conversation with her by typing, all going well it should go something like this:
Me: "open banking skill" (Or whatever the name of your skill is)
Alexa: "Welcome to your example credit card. Why don't you ask me about your account information or pending transactions."
Me: "account information"
Alexa: "This account is a capitalone credit card and the card number associated with it ends in XXXX"
Me: "pending transactions"
Alexa: "Of the last X transactions, a total of X are pending"


Mic. Drop. There you have it folks, a super simple Alexa skill pieced together using Lambda & Python. Why don't you take a closer look at the code to see how it's done, or try expanding your function to introduce some new features.

The ability of the CapitalOne API we're using is still in it's infancy, but as that's built out I'll continue to add new features to this tutorial.

Disclaimer: I am _not_ a Python dev nor do I claim to be, this tutorial was the begining of my Python days so please feel free to critique. If you'd like to expand on this or contribute just get in touch or throw in a PR.
