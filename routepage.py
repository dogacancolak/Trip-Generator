# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import Screen
import random
from math import sin, cos, sqrt, atan2, radians, ceil
from api_call import get_places_in_radius
import timeit
import urllib.request
import json
import sys
import itertools

class RoutePage(Screen):

    interest_places = None
    food_places = None
    def generate_trip(self): 
        
        user_info =  App.get_running_app().user_info

        print("entering first api call", file=sys.stderr)
        self.interest_places = get_places_in_radius(user_info, user_info.interests)
        self.food_places     = get_places_in_radius(user_info, user_info.food)
        print("exiting first api call", file=sys.stderr)
        
        place_number_hint = ceil(user_info.trip_length / 60 * 1.3)
         # approximately 1.4 places per hour

        print("adding waypoints", file=sys.stderr)

        waypoints = []
        for key in self.food_places:
            while True:
                place = random.choice(self.food_places[key])    
                if all(point['name'] != place['name'] for point in waypoints):
                    waypoints.append(place)
                    place_number_hint -= 1
                    break

        print("adding interests", file=sys.stderr)

        for _ in range(place_number_hint):
            added = self.add_waypoint(waypoints)
            if not added:
                break
        print("find directions", file=sys.stderr)
                
        route_details = self.optimize_route(waypoints)
        route = route_details[0]
        time_spent = route_details[1]
        print("while loops", file=sys.stderr)

        entered = False
        while time_spent > user_info.trip_length + 15:
            removed = self.remove_waypoint(waypoints)
            if not removed:
                break
            else:
                route_details = self.optimize_route(waypoints)
                route = route_details[0]
                time_spent = route_details[1]
            entered = True
            print("trip length too long", file=sys.stderr)

        if not entered:
            while time_spent < user_info.trip_length - 40:
                added = self.add_waypoint(waypoints)
                if not added:
                    break
                else:
                    route_details = self.optimize_route(waypoints)
                    route = route_details[0]
                    time_spent = route_details[1]
                   
                print("trip length too short", file=sys.stderr)

        print("ordered:")
        for i in route['waypoint_order']:
            print(waypoints[i]['name'])

        print("Time spent: ", time_spent/60, file=sys.stderr)
        
    def optimize_route(self, waypoints):

        shortest = 100000
        for point in waypoints:
            temp_route = self.find_directions(waypoints, point)
            time = self.calculate_time(temp_route)
            if time < shortest:
                route = temp_route
                shortest = time

        return (route, shortest)

    def calculate_time(self, route):
        leg_duration = 0
        for route_index in range(len(route["legs"]) - 1):
            leg_duration += route["legs"][route_index]["duration"]["value"]/60

        return leg_duration + len(route["waypoint_order"]) * 40

    # If successfully removed a waypoint, returns True
    # If cannot remove any more waypoints, returns False
    def remove_waypoint(self, waypoints):
        if not waypoints:
            return False
        food_count = len(self.food_places)
        if waypoints[food_count:] != []:
            waypoint = random.choice(waypoints[food_count:])
        else:
            waypoint = random.choice(waypoints)
        waypoints.remove(waypoint)
        return True
        
    # If successfully added a waypoint, returns True
    # If cannot add any more waypoints, returns False
    def add_waypoint(self, waypoints):
        while True:
            if not self.interest_places:
                return False
            else:
                key = random.choice(list(self.interest_places))
                place = random.choice(list(self.interest_places[key]))
                self.interest_places[key].remove(place)
                if not self.interest_places[key]:
                    del self.interest_places[key]
                if all(point['name'] != place['name'] for point in waypoints) and \
                    'restaurant' not in place['types']:
                    waypoints.append(place)
                    return True                    

    def find_directions(self, waypoints, destination):
        
        user_info =  App.get_running_app().user_info
        user_loc = str(user_info.lat) + ',' + str(user_info.lon)
        
        transportation = user_info.transportation
        
        if transportation == 'cycling' or transportation == 'walking':
            avoid = "&avoid=highways"
        else:
            avoid = ''

        api_waypoints = ''
        for point in waypoints:
            api_waypoints += 'place_id:' + point['place_id'] + '|'
            
        endpoint       = 'https://maps.googleapis.com/maps/api/directions/json?'
        key            = 'AIzaSyA4H5RbPwYejTlXVI1hjio_4q4XYS_Ubts'
        nav_request    = 'origin={}&destination=place_id:{}&mode={}{}&waypoints=optimize:true|{}&key={}'\
                            .format(user_loc, destination['place_id'], \
                                    transportation, avoid, api_waypoints, key)

        response = json.loads(urllib.request.urlopen(endpoint + nav_request).read())

        if response['status'] == 'OK':
            route = response['routes'][0]
            return route
        else:
            print("no route found")


    # def remove_duplicates(self, dict_raw):
    #     filtered_dict = {}
    #     for key in dict_raw:
    #         # print("key is: ", key, file=)
    #         filtered_list = []
    #         for p in dict_raw[key]:
    #             duplicate = False
    #             if p in itertools.chain(*filtered_dict.values()):
    #                     duplicate = True
    #                     break
    #             if not duplicate:
    #                 if 'restaurant' not in p['types'] or p in itertools.chain(*self.food_places.values()):
    #                     filtered_list.append(p)
    #         if filtered_list:
    #             filtered_dict[key] = filtered_list

    #     dict_raw = filtered_dict