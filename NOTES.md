# Database Schema
```
Teacher {teacher_id, teacher_first_name, teacher_surname, teacher_subject}

Parent {parent_id, student_id*, parent_first_name, parent_surname}

Student {student_id, student_first_name, student_surname, class_id*}

Class {class_id, class_number, class_name, class_floor}

ParentBooking {teacher_id, student_id, parent_id, booking_date, booking_time}
```


