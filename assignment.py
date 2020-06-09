import numpy as np

INF = 1000000

def data_generation(machine_type, time, machines, country_prices):
  '''
  Data cleaning of empty value 
  and generating rates for the given number of hours
  '''
  new_machine_type=[]
  new_machines=[]
  new_country_prices=[]  
  for i in range(len(machines)):
    if country_prices[i] != None:
      new_machine_type.append(machine_type[i])      
      new_machines.append(machines[i])      
      new_country_prices.append(country_prices[i] * time)

  return new_machine_type, new_machines, new_country_prices      


def minimum_cost_resource_allocator(country, machine_type, machines, country_prices, units):
  '''
  Main function to find minimum_cost_resource distribution
  '''
  n = len(country_prices)
  # Solution matrix initialization
  solution_matrix = [[None for j in range(units+1)] for i in range(n+1)] 
  for i in range(0, n+1):
    for j in range(units+1):
      # Base cases
      if j==0 and i>0:
        solution_matrix[i][j]=0

      elif i==0:  
        solution_matrix[i][j]=INF

  for i in range(1, n+1):
    for j in range(1, units+1):

      if machines[i-1]<=j:
        solution_matrix[i][j] = min( country_prices[i-1] + solution_matrix[i][j-machines[i-1]], 
                                    solution_matrix[i-1][j])
      else:
        solution_matrix[i][j] = solution_matrix[i-1][j]

  lowest_weight = solution_matrix[n][units]
  machines_with_qty = find_machines(solution_matrix, n, machine_type, machines, units, country_prices)
  
  # Output in the format 
  output = {
  "region": country,
  "total_cost": "$"+str(lowest_weight),
  "machines": list(zip(machines_with_qty.keys(), machines_with_qty.values())) 
  }
  return output

def find_machines(dp, n, machine_type, machines, units, country_prices):
  '''
  Function to track the matrix and 
  find the machines and their respective quantities
  acheiving the otpimal results
  '''
  x = n
  y = units
  hash = dict()
  while (x > 0 and y > 0):
    if dp[x][y] == dp[x - 1][y]:
        x-=1
    elif (dp[x - 1][y] == dp[x][y - machines[x - 1]] + country_prices[x - 1]): 
        x-=1
    else:
      if machine_type[x - 1] in hash.keys():
        hash[machine_type[x - 1]] += 1
      else:
        hash[machine_type[x - 1]] = 1      
      # print("including wt " + str(machines[x - 1]) + " with value " + str(country_prices[x - 1]))
      y -= machines[x - 1]
  return hash


def resource_allocator(units, time):
  '''
  Main resource allocator function  
  '''
  countries= ["NewYork", "India", "China"]
  NewYork  = [120,230,450,774,1400,2820]
  India    = [140,None,413,890,1300,2970]		
  China    = [110,200,None,670,1180,None]
  allocated_resource=[]

  for country in countries:
    machine_type = ['Large', 'XLarge', '2XLarge', '4XLarge', '8XLarge', '10XLarge']
    machines = [10, 20, 40, 80, 160, 320]	
    country_pricelist = [NewYork, India, China]
    country_and_price = dict(zip(countries, country_pricelist))

    machine_type, machines, country_prices = data_generation(machine_type, time, machines, country_and_price[country])
    allocated_resource.append( minimum_cost_resource_allocator(country, machine_type, machines, country_prices, units) )
  
  print({
      "Output" : allocated_resource
      })


if __name__ == "__main__":
  '''
  Main calling function
  '''
  units = int(input("Capacity (units): "))
  time = int(input("Operation time (hours): "))
  resource_allocator(units, time)
