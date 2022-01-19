SERVICES_PROVIDED = {'change_oil': 2, 'inflate_tires': 5, 'diagnostic': 30}
class Ticket:
    ticket_counter = 0

    def __init__(self, service):
        Ticket.ticket_counter += 1
        self.id = Ticket.ticket_counter
        self.service = service
        self.wait_time = 0

    def __str__(self):
        return f'id:{self.id}\nwait_time:{self.wait_time}\nservice:{self.service}'

    # def __repr__(self):
    #     return f'id:{self.id}\nwait_time:{self.wait_time}\nservice:{self.service}'


class LineOfCars:
    current_line = {'change_oil': [], 'inflate_tires': [], 'diagnostic': []}
    services_provided = SERVICES_PROVIDED

    def __init__(self):
        self.whole_que_wait_time = 0

    def add_ticket_to_line(self, ticket):
        self.current_line[ticket.service].append(ticket)
        self.calculate_wait_times()

    def calculate_wait_times(self):
        wait_time = 0
        for service in self.services_provided:
            for ticket in self.current_line[service]:
                ticket.wait_time = wait_time
                wait_time += self.services_provided[service]
        self.whole_que_wait_time = wait_time
