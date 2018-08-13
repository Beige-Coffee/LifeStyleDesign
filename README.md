# LifeStyleDesign
LifeStyleDesign is a script that help's students efficiently pay off debt while also enjoying the city in which they live.

## Motivation
The purpose of LifeStyleDesign is to challenge the user (in this case, a student) to take part in actively building their life. In doing this, the driver is forced to confront new obstacles that they may have otherwise overlooked and, throughout this process, they achieve a deeper level of insight into the objective at hand. For all of the aforementioned reasons, I built LifeStyleDesign to empower individuals to take hold of the data at hand and leverage it to model *all the possible worlds* they may inhabit. In this case, I have modeled **116** distinct worlds to gain insight regarding an obstacle that many students in today's economy face - namely, **debt**. 

Over the course of the comming weeks, I will be cleaning up the code so that it is more usable and interpretable as well as adding further insights that I tease out of this exercise. However, I strategically chose to make my work public because I firmly believe that, in this case, the philosophy behind the project is just as important (if not more important) than the code behind the project. With a bit of Existentialist flair, the purpose of this endeavor is not for a user to blindly copy the code but, instead, for a user to strategically and analytically evaluate the choice at hand and make strides to achieve a predetermined goal. This, in essence, is LifeStyleDesign. 

## Quick-Vew Of Parameters
  - Cost-of-living for hand-chosen cities
  - My specific monthy expenditures (cups of coffee per month, gym memberships, rent, gas, groceries, etc.)
  - Predicted salary for entry-level data scienctist - specific for each city
  - Income tax for each city

## Detailed Look Into Parameters
To develop my model, I use Selenium to scrape the following information off the internet:
  - Cost-of-living data for 29 predetermined cities
    - This number is somewhat arbitrary. I'll admit that I am not actually considering moving to all 29 cities, however, I was mainly interested to see how each city compared to a plethora of diverse locations across the country.
    - Cost of living data was scraped from www.numbeo.com/cost-of-living/
  - The user-specific monthly expenditures that characterize my lifestyle
    - I manually went through this data and created a **monthly constant** variable, which allowed me to calculate an estimated cost-of-living that is specific to my lifestyle. For example, monthly constant I included where:
      - Number of Cups of Coffee Per Month
      - Taxis/Ubers 
      - Gas
      - Rent (including water, electricity, etc.)
      - And more...
- Data Science salaries for each of these 29 cities
  - An important design decision was made here. Namely, I chose to take the **lower end** of the range for data science salaries. I did this because I am relatively fresh out of college and just begining my journey into data science. Therefore, I did not want to assume my salary to be closer to the average (which is usually around $100,000) and skew my model.
   - All salary data was scraped from Glassdoor.com

- To further increase the accuracy of my predictions, I chose to include each city's state income tax so that I could accordingly adjust my income for each city. As of now, I manually coded each state's income tax, standard deduction, and personal exemption. For the purposes of my model, I only inlcuded the information that reflected my predicted salary in each city. In the comming weeks, I will work to make a function that can do this algorithmically.
    - This information can be found here: https://files.taxfoundation.org/20180315173118/Tax-Foundation-FF576-1.pdf


# Data Visualization
Let's look at some graphs!
<img width="834" alt="screen shot 2018-08-12 at 11 06 54 am" src="https://user-images.githubusercontent.com/34213201/44036537-de037e1e-9ec6-11e8-94af-adc1ba20a60a.png">

After all is said and done, I executed some calculations on the aforementioned data points and was able to graph the number of years it would take me to pay off my debt. To do this, I calculated my monthly net income for each city and assumed I would allocate roughly %30 to debt. Subsequently, I determined how long it would take me to pay off my debt, assuming that I chose to live in a 1-bedroom apparment in the center of the city. This graph displays the resulting calcuations. A quick note of interest: it's interesting how we all know that NYC is extremely expensive, however, it resonates on a deeper level when you actually see NYC *tower* above all of the other cities. It just goes to show how powerful and ingrained human vision is in our emotions.


<img width="785" alt="screen shot 2018-08-12 at 3 33 54 pm" src="https://user-images.githubusercontent.com/34213201/44036543-e07607ca-9ec6-11e8-885b-8c3e34362e7e.png">
