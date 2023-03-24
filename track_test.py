import json
import datetime

#不正な入力エラー
bad_input_error = {
  "code": 999
}


#端末操作エラー
terminal_operation_error = {
  "code": 99
}


#ワンドリンクエラー
one_drink_error = {
  "code": 1,
  "price": 0,
  "drink": 0
}

#正常
correct_answer = {
  "code": 0,
  "price": 0
}

class Karaoke_Room_rate_Calculation_System():
    def __init__(self):
        self.record_array= []
        self.leave_record_array = []
        self.total_number_of_people_in_the_room = 0
        self.total_number_of_people_leaving = 0
        self.current_number_of_people_in_the_room = 0
        self.total_number_of_room_rate = 0
        self.total_number_of_drinks_ordered = 0
        self.total_price_of_drinks_ordered = 0
        self.total_fee_of_food = 0
        
        
        


    def calculate_karaoke_room_rates(self):
        
        create_record = self.create_record_array()
        
        if create_record == bad_input_error:
            bad_input_error_json_object = json.dumps(bad_input_error)
            return bad_input_error_json_object

        for record in self.record_array:
    
            if 'header one_drink' in self.record_array[0]:

                price_per_30_minutes_for_one_drink_during_day_time = 100
                price_per_30_minutes_for_one_drink_during_night_time = 400

                if 'enter' in record :         
                    self.calculate_room_rate(record, self.record_array[-1], price_per_30_minutes_for_one_drink_during_day_time, price_per_30_minutes_for_one_drink_during_night_time)
                   
                    if 1000 <= self.total_number_of_people_in_the_room:
    
                        return terminal_operation_error_json_object


                if 'leave' in record:
                    number_of_people_leaving = int(record.split()[-1])
                    self.total_number_of_people_leaving += number_of_people_leaving
                    if self.total_number_of_people_in_the_room < self.total_number_of_people_leaving:
                        terminal_operation_error_json_object = json.dumps(terminal_operation_error)
                        return terminal_operation_error_json_object          
                            

                if 'drink soft_drink' in record or 'drink alcohol' in record:
                    self.calculate_drink_rate(record)          


                if 'food' in record:
                    self.calculate_food_rate(record)   

                    
                if 'footer' in record:
                    if self.total_number_of_drinks_ordered < self.total_number_of_people_in_the_room:
                        one_drink_error['price'] = self.total_number_of_room_rate + self.total_price_of_drinks_ordered + self.total_fee_of_food
                        one_drink_error['drink'] = self.total_number_of_people_in_the_room - self.total_number_of_drinks_ordered
                        one_drink_error_json_object = json.dumps(one_drink_error)
 
                        return one_drink_error_json_object
                    
                    else:
                        answer = self.total_number_of_room_rate + self.total_price_of_drinks_ordered + self.total_fee_of_food
                        correct_answer['price'] = answer
                        correct_answer_json_object = json.dumps(correct_answer)

                        return correct_answer_json_object
                
            elif 'header free_refills' in self.record_array[0]:

                price_per_30_minutes_for_free_refills_during_day_time = 200
                price_per_30_minutes_for_free_refills_during_night_time = 500
                
                if 'enter' in record :
                    self.calculate_room_rate(record, self.record_array[-1], price_per_30_minutes_for_free_refills_during_day_time, price_per_30_minutes_for_free_refills_during_night_time)
                    
                    if 1000 <= self.total_number_of_people_in_the_room:
                        terminal_operation_error_json_object = json.dumps(terminal_operation_error)
                        return terminal_operation_error_json_object

                
                if 'leave' in record:
                    number_of_people_leaving = int(record.split()[-1])
                    self.total_number_of_people_leaving += number_of_people_leaving
                    if self.total_number_of_people_in_the_room < self.total_number_of_people_leaving:
                        terminal_operation_error_json_object = json.dumps(terminal_operation_error)
                        return terminal_operation_error_json_object

                   
                if 'drink alcohol' in record:
                    self.calculate_drink_rate(record)
                    

                if 'food' in record:
                    self.calculate_food_rate(record)

                    
                if 'footer' in record:
                    answer = self.total_number_of_room_rate + self.total_price_of_drinks_ordered + self.total_fee_of_food
                    correct_answer['price'] = answer
                    correct_answer_json_object = json.dumps(correct_answer)

                    return correct_answer_json_object

            elif 'header alcohol_free_refills' in self.record_array[0]: 

                price_per_30_minutes_for_alcohol_free_refills_during_day_time = 300
                price_per_30_minutes_for_alcohol_free_refills_during_night_time = 650

                if 'enter' in record:            
                    self.calculate_room_rate(record, self.record_array[-1], price_per_30_minutes_for_alcohol_free_refills_during_day_time, price_per_30_minutes_for_alcohol_free_refills_during_night_time)

                    if 1000 <= self.total_number_of_people_in_the_room:
                        terminal_operation_error_json_object = json.dumps(terminal_operation_error)
                        return terminal_operation_error_json_object

                
                if 'leave' in record:
                    number_of_people_leaving = int(record.split()[-1])
                    self.total_number_of_people_leaving += number_of_people_leaving
                    if self.total_number_of_people_in_the_room < self.total_number_of_people_leaving:
                        terminal_operation_error_json_object = json.dumps(terminal_operation_error)
                        return terminal_operation_error_json_object


                if 'food' in record:
                    self.calculate_food_rate(record)
                    

                if 'footer' in record:
                    answer = self.total_number_of_room_rate + self.total_price_of_drinks_ordered + self.total_fee_of_food
                    correct_answer['price'] = answer
                    correct_answer_json_object = json.dumps(correct_answer)

                    return correct_answer_json_object


    def create_record_array(self):
        base_time = '08:00:00'

        while True:
            record = input()
            time_to_compare = record.split()[0]
            
            if ' ' in record[-1]:
                return bad_input_error

            if not len(record) <= 1000:
                return bad_input_error

            if time_to_compare < base_time:
                return bad_input_error
                
            if 'header' in record:
                header_record = record.split()
                
                if len(header_record) != 3:
                    return bad_input_error
            
            if 'enter' in record:
                number_of_people_in_the_room = int(record.split()[-1])
                if not 1 <= number_of_people_in_the_room <= 999:
                    return bad_input_error
                
                    

            if 'leave' in record:
                number_of_people_leaving = int(record.split()[-1])
                if not 1 <= number_of_people_leaving <= 999:
                    return bad_input_error

                else:
                    self.leave_record_array.append(record)

                
            if 'drink soft_drink' in record or 'drink alcohol' in record:
                price_of_drinks_ordered = int(record.split()[-2])
                number_of_drinks_ordered = int(record.split()[-1])

                if not 1 <= price_of_drinks_ordered <= 9999:
                    return bad_input_error
                    
                elif not 1 <= number_of_drinks_ordered <= 99:
                    return bad_input_error
                    

            self.record_array.append(record)

            base_time = time_to_compare
             
            if 'footer' in record:

                break

    
    def calculate_room_rate(self, record, footer_record, price_per_30_minute_during_day_time, price_per_30_minute_during_night_time):
        

        footer_time = footer_record.split()[0]
        
        footer_time_split = footer_time.split(':')
        
        footer_time = datetime.timedelta(hours=int(footer_time_split[0]), minutes=int(footer_time_split[1]), seconds=int(footer_time_split[2]))
        

        
        #入室時刻
        entering_time = record.split()[0]
          
        # 入室時刻リストを分割
        entering_time_split = entering_time.split(':')

        
        #現在の時刻
        current_time = datetime.timedelta(hours=int(entering_time_split[0]), minutes=int(entering_time_split[1]), seconds=int(entering_time_split[2]))
          
        # 入室人数

        number_of_people_in_the_room = int(record.split()[-1])

        self.total_number_of_people_in_the_room += number_of_people_in_the_room

        self.current_number_of_people_in_the_room = number_of_people_in_the_room


        # counter変数
        
        count = 1
        

        while True:  
            
            time_to_footer = self.Subtract_current_time_and_footer_or_leave_time(current_time, footer_time)
            
                  
            if entering_time <= '16:59:59':
                if current_time <= datetime.timedelta(hours=18, minutes=49, seconds=59):

                    add_or_break = self.add_to_total_number_of_room_rate(count, footer_time, current_time, time_to_footer, price_per_30_minute_during_day_time)
                    if add_or_break == 'break':
                        break
                        
                elif datetime.timedelta(hours=18, minutes=50, seconds=0) <= current_time:
    
                        add_or_break = self.add_to_total_number_of_room_rate(count, footer_time, current_time, time_to_footer, price_per_30_minute_during_night_time)
                        if add_or_break == 'break':
                            break

            elif '17:00:00' <= entering_time:
                if current_time <= datetime.timedelta(hours=17, minutes=49, seconds=59):
    
                    add_or_break = self.add_to_total_number_of_room_rate(count, footer_time, current_time, time_to_footer, price_per_30_minute_during_day_time)
                    if add_or_break == 'break':
                        break


                if datetime.timedelta(hours=17, minutes=50, seconds=0) <= current_time:

                    s = self.add_to_total_number_of_room_rate(count, footer_time, current_time, time_to_footer, price_per_30_minute_during_night_time)
                    if s == 'break':
                        break

                
            current_time = current_time + datetime.timedelta(minutes=30)

            count += 1             
        

    
    def Subtract_current_time_and_footer_or_leave_time(self, current_time, footer_or_leave_time):
        answer = footer_or_leave_time - current_time

        return answer
    
    def add_to_total_number_of_room_rate(self, count, footer_time, current_time, time_to_footer, price_per_30_minute):
        
       
        if count == 1:
            
            self.total_number_of_room_rate += price_per_30_minute * self.current_number_of_people_in_the_room
        
        else:
            
            if not len(self.leave_record_array) == 0:

                    leave_time_split = self.leave_record_array[0].split()[0].split(':')
                   
                    leave_time = datetime.timedelta(hours=int(leave_time_split[0]), minutes=int(leave_time_split[1]), seconds=int(leave_time_split[2]))
                  
                    leaving_peple = int(self.leave_record_array[0].split()[-1])
                    
                    time_to_leave = self.Subtract_current_time_and_footer_or_leave_time(current_time, leave_time)
                    

                    if time_to_leave <= datetime.timedelta(minutes=10):
                        
                        self.current_number_of_people_in_the_room -= leaving_peple
                        
     
                        if 0 == self.current_number_of_people_in_the_room:

                            del self.leave_record_array[0]

                            return 'break'
                        
                        elif 0 < self.current_number_of_people_in_the_room:

                            del self.leave_record_array[0]

                        else:
                            leaving_peple = int(self.leave_record_array[0].split()[-1])
                           
                            self.leave_record_array[0] = self.leave_record_array[0][:-1] + str(abs(self.current_number_of_people_in_the_room))

                            return 'break'

                    elif leave_time <= current_time:
                        self.total_number_of_room_rate += price_per_30_minute * self.current_number_of_people_in_the_room

                        self.current_number_of_people_in_the_room -= leaving_peple
                  

                        if 0 == self.current_number_of_people_in_the_room:
                            del self.leave_record_array[0]

                            return 'break'

                        elif 0 < self.current_number_of_people_in_the_room:
                            del self.leave_record_array[0]

                        else:
                            leaving_peple = int(self.leave_record_array[0].split()[-1])
                           
                            self.leave_record_array[0] = self.leave_record_array[0][:-1] + str(abs(self.current_number_of_people_in_the_room))

                            return 'break'

            if time_to_footer <= datetime.timedelta(minutes=10):
                return 'break'
            
            else:
                self.total_number_of_room_rate += price_per_30_minute * self.current_number_of_people_in_the_room

                if footer_time <= current_time:
                   return 'break' 
                

    def calculate_food_rate(self, record):
        price_of_food = int(record.split()[-2])
        number_of_foods = int(record.split()[-1])
        food_order_fee = price_of_food * number_of_foods

        self.total_fee_of_food += food_order_fee


    def calculate_drink_rate(self, record):
        number_of_drinks_ordered = int(record.split()[-1])
        the_price_of_each_drink_ordered = int(record.split()[-2])
        the_price_of_the_drink_ordered = the_price_of_each_drink_ordered * number_of_drinks_ordered

        self.total_number_of_drinks_ordered += number_of_drinks_ordered
        self.total_price_of_drinks_ordered += the_price_of_the_drink_ordered


karaoke_room_rate_calculation_system = Karaoke_Room_rate_Calculation_System()
answer = karaoke_room_rate_calculation_system.calculate_karaoke_room_rates()
print(answer)


