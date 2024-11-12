from django.db import models
import csv
from datetime import datetime
import os

class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=10)
    precinct_number = models.CharField(max_length=10)

    voted_2020_state = models.BooleanField(default=False)
    voted_2021_town = models.BooleanField(default=False)
    voted_2021_primary = models.BooleanField(default=False)
    voted_2022_general = models.BooleanField(default=False)
    voted_2023_town = models.BooleanField(default=False)

    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Precinct {self.precinct_number}"
    
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', 'newton_voters.csv')
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        datareader = csv.DictReader(csvfile)
        voters = []
        for row in datareader:
            party = row['Party Affiliation'].strip()
            def to_bool(value):
                return value.strip().lower() == 'true'

            voter = Voter(
                last_name=row['Last Name'].strip(),
                first_name=row['First Name'].strip(),
                street_number=row['Residential Address - Street Number'].strip(),
                street_name=row['Residential Address - Street Name'].strip(),
                apartment_number=row['Residential Address - Apartment Number'].strip() or None,
                zip_code=row['Residential Address - Zip Code'].strip(),
                date_of_birth=datetime.strptime(row['Date of Birth'].strip(), '%Y-%m-%d').date(),
                date_of_registration=datetime.strptime(row['Date of Registration'].strip(), '%Y-%m-%d').date(),
                party_affiliation=party,
                precinct_number=row['Precinct Number'].strip(),
                voted_2020_state=to_bool(row['v20state']),
                voted_2021_town=to_bool(row['v21town']),
                voted_2021_primary=to_bool(row['v21primary']),
                voted_2022_general=to_bool(row['v22general']),
                voted_2023_town=to_bool(row['v23town']),
                voter_score=int(row['voter_score'].strip())
            )
            voters.append(voter)
        Voter.objects.bulk_create(voters)
