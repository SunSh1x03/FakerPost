from faker import Faker
from time import sleep
import requests
import socket

faker = Faker()

name= (faker.first_name() + '.' + faker.last_name())
senha= faker.password()
country1= faker.country()
useragent= faker.user_agent()
pload= { 'username':  name , 'password': senha }
pload2= {  'User-Agent': useragent , 'Country': country1 }

r = requests.post('https://site1.com/efetuar-login.php', data = pload , headers = pload2, allow_redirects=False)
#r = requests.post('https://site2.com/login.php', data = pload , headers=pload2 , allow_redirects=False)

sleep(0.05)
