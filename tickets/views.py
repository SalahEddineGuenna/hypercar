from collections import deque

from django.views import View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

active_client_identifier = ''


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f"<h2>Welcome to the Hypercar Service!</h2>")


class MenuView(View):
    template_name = "tickets/menu.html"

    def get(self, request, *args, **kwargs):
        menu = {"change_oil": "Change oil",
                "inflate_tires": "Inflate tires",
                "diagnostic": "Diagnostic", }
        return render(request, 'menu.html', {"menu": menu})


ticket_services = {"change_oil": 0,
                   "inflate_tires": 0,
                   "diagnostic": 0}


class QueueHandler(View):
    template_name = "tickets/ticket.html"
    tickets = []
    time_to_wait = []
    change_oil_queue = deque()
    inflate_tires_queue = deque()
    diagnostic_queue = deque()
    services = {"change_oil": {"queue": change_oil_queue, "time": 2},
                "inflate_tires": {"queue": inflate_tires_queue, "time": 5},
                "diagnostic": {"queue": diagnostic_queue, "time": 30}}

    def get(self, request, *args, **kwargs):
        request_url = request.path_info
        service = [item for item in self.services.keys() if item in str(request_url)][0]
        ticket = self.get_new_ticket(service)
        return render(request, self.template_name,
                      {"ticket_number": ticket, "minutes_to_wait": self.count_time(ticket, service)})

    def count_time(self, user_ticket, user_service):
        time_counter = 0
        if len(self.tickets) <= 2:
            self.time_to_wait.append(self.services[user_service]["time"])
            return time_counter
        if user_ticket == 3:
            return min(self.time_to_wait)
        for service in self.services.keys():
            time_counter += self.services[service]["time"] * len(self.services[service]["queue"])
            if user_ticket in self.services[service]["queue"]:
                time_counter -= self.services[service]["time"]
                break
        return time_counter

    def get_new_ticket(self, user_service):
        ticket = len(self.tickets) + 1
        self.tickets.append(ticket)
        self.services[user_service]["queue"].append(ticket)
        ticket_services[user_service] += 1
        return ticket

    def dequeue(self, service):
        self.services[service]["queue"].popleft()


class ProcessQueue(View):
    template_name = "tickets/processing.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"oil": ticket_services["change_oil"],
                                                    "tire": ticket_services["inflate_tires"],
                                                    "diagnostic": ticket_services["diagnostic"]})

    @staticmethod
    def post(request):
        for action in QueueHandler.services:
            if QueueHandler.services[action]["queue"]:
                global active_client_identifier
                active_client_identifier = QueueHandler.services[action]["queue"].popleft()
                break
            active_client_identifier = ''
        return redirect('/next')


class NextTicket(View):
    template_name = "tickets/next.html"

    def get(self, request):
        return render(request, self.template_name, {"active_client": active_client_identifier})