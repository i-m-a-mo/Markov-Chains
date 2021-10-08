
import pandas as pd
import numpy as np


class Supermarket:


    def __init__(self, first_spawn, custperhour, cust_locations_probability):

        self.last_id = 0
        self.customers = []
        self.minutes = 0
        self.max_customers = 3
        self.feierabend = 840
        self.customers_recording = pd.DataFrame(columns=['customerID', 'location', 'minutes'])
        self.customer_spawn = first_spawn
        self.customer_fillrate = custperhour
        self.customer_locations_prob = cust_locations_probability

    def __repr__(self):
        return self.customers
        #return f"The customers in the supermarket are {self.customers}."

    def print_customers(self):
        """print all customers with the current time and id in CSV format.
        """
        self.customers_recording.to_csv(f'customers_after_{self.minutes}_minutes')

    def customer_info(self):
        """Show all customers and their current location"""

        for c in range(0,len(self.customers)):
            print (f"The customer {self.customers[c]} is in section {self.customers[c].location}.")

    def time_of_day_customer_mass(self):
        """Sets maximum number of customers according to hour of the day. Needs dataframe with Customernumbers per hour"""
        hour_of_day = round((420+self.minutes)/60)   #self.minutes
        if hour_of_day in self.customer_fillrate.index:
            self.max_customers = round(self.customer_fillrate.iloc[hour_of_day]['sum']*0.005) #downscaled for grafical simulation


    def next_minute(self):
        """propagates all customers to the next state.
        """
        self.time_of_day_customer_mass()
        self.minutes += 1
        if self.minutes < self.feierabend:
            for c in range(0,len(self.customers)):
                self.customers_recording = self.customers_recording.append({'customerID':self.customers[c], 'location':self.customers[c].location, 'minutes':self.minutes}, ignore_index=True)

            self.remove_customers()

            for c in range(0,len(self.customers)):
                self.customers[c].change_location()

            self.add_new_customers()

        else:
            self.termination()

    def go_shopping(self, shopping_time):
        """Simulate all the minute steps until the feierabend-value is reached
            Needs number of minutes (int) as an argument
        """
        self.feierabend = shopping_time
        for t in range(0,self.feierabend):
            self.next_minute()

    def termination(self):
        for c in range(0,len(self.customers)):
            self.customers_recording = self.customers_recording.append({'customerID':self.customers[c], 'location':'checkout', 'minutes':self.minutes}, ignore_index=True)
        self.customers = []
        print('the supermarket is now closed')

    def add_new_customers(self):
        """creates new customers depending on the max customer number.
        """
        while (len(self.customers) < self.max_customers):
            self.last_id += 1
            customer = Customer(f"cust_id{self.last_id}", self.customer_spawn, self.customer_locations_prob)
            self.customers.append(customer)

    def remove_customers(self):
        """removes every customer that is not active any more.
            and save the ID, last location and timestamp to a dataframe (former_customers)
        """
        buffer = []
        for c in range(0,len(self.customers)):
            if self.customers[c].location != 'checkout':
                buffer.append(self.customers[c])
        self.customers = buffer




class Customer:

    def __init__(self, customer_name, customer_spawn, location_probability):

        self.name = customer_name
        self.location = np.random.choice(['dairy','fruit','drinks','spices'], p=customer_spawn)
        self.loc_sequence = []
        self.probs = location_probability
        self.possible_locations = ['checkout', 'dairy', 'drinks', 'fruit', 'spices']


    def __repr__(self):
        return self.name


    def change_location(self):
        self.location = np.random.choice(self.possible_locations, p=self.probs.loc[self.location])
