from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Voter
from django.db.models import Q
import plotly.express as px
from django.views.generic import TemplateView
from django.db.models import Count

# Create your views here.

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_date_of_birth')
        max_dob = self.request.GET.get('max_date_of_birth')
        voter_score = self.request.GET.get('voter_score')
        voted_elections = self.request.GET.getlist('voted_elections')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if voted_elections:
            q_objects = Q()
            for election in voted_elections:
                q_objects &= Q(**{election: True})
            queryset = queryset.filter(q_objects)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['years'] = range(1900, datetime.now().year + 1)
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')
        context['elections'] = [
            {'field_name': 'voted_2020_state', 'display_name': '2020 State'},
            {'field_name': 'voted_2021_town', 'display_name': '2021 Town'},
            {'field_name': 'voted_2021_primary', 'display_name': '2021 Primary'},
            {'field_name': 'voted_2022_general', 'display_name': '2022 General'},
            {'field_name': 'voted_2023_town', 'display_name': '2023 Town'},
        ]
        context['selected_voted_elections'] = self.request.GET.getlist('voted_elections')
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphsView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = Voter.objects.all()

        voters = self.apply_filters(voters)

        birth_years = voters.values_list('date_of_birth', flat=True)
        birth_years = [dob.year for dob in birth_years]
        fig1 = px.histogram(
            x=birth_years,
            nbins=100,
            labels={'x': 'Year of Birth', 'y': 'Count'},
            title='Voters by Year of Birth'
        )
        graph1 = fig1.to_html(full_html=False)

        party_counts = voters.values('party_affiliation').annotate(count=Count('party_affiliation'))
        fig2 = px.pie(
            names=[party['party_affiliation'] for party in party_counts],
            values=[party['count'] for party in party_counts],
            title='Voters by Party Affiliation'
        )
        graph2 = fig2.to_html(full_html=False)

        elections = [
            {'field_name': 'voted_2020_state', 'display_name': '2020 State'},
            {'field_name': 'voted_2021_town', 'display_name': '2021 Town'},
            {'field_name': 'voted_2021_primary', 'display_name': '2021 Primary'},
            {'field_name': 'voted_2022_general', 'display_name': '2022 General'},
            {'field_name': 'voted_2023_town', 'display_name': '2023 Town'},
        ]
        participation = {}
        for election in elections:
            count = voters.filter(**{election['field_name']: True}).count()
            participation[election['display_name']] = count

        fig3 = px.bar(
            x=list(participation.keys()),
            y=list(participation.values()),
            labels={'x': 'Election', 'y': 'Number of Voters'},
            title='Voting Participation by Election'
        )
        graph3 = fig3.to_html(full_html=False)

        context['graph1'] = graph1
        context['graph2'] = graph2
        context['graph3'] = graph3

        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        current_year = datetime.now().year
        context['years'] = range(1900, current_year + 1)
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')
        context['elections'] = elections
        context['selected_voted_elections'] = self.request.GET.getlist('voted_elections')

        context['selected_party'] = self.request.GET.get('party_affiliation', '')
        context['selected_min_dob'] = self.request.GET.get('min_date_of_birth', '')
        context['selected_max_dob'] = self.request.GET.get('max_date_of_birth', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')

        return context

    def apply_filters(self, queryset):
        party = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_date_of_birth')
        max_dob = self.request.GET.get('max_date_of_birth')
        voter_score = self.request.GET.get('voter_score')
        voted_elections = self.request.GET.getlist('voted_elections')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if voted_elections:
            q_objects = Q()
            for election in voted_elections:
                q_objects &= Q(**{election: True})
            queryset = queryset.filter(q_objects)
        return queryset