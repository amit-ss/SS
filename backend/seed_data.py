import os
import django
from datetime import datetime, date, time, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import StudentProfile
from timetable.models import Faculty, Course, ClassTimetable, ExamSchedule
from attendance.models import SubjectAttendance
from navigation.models import CampusLocation
from events.models import CampusEvent
from lost_found.models import LostFoundItem
from career.models import InterviewQuestion, CareerProfile
from notifications.models import Notification
from chatbot.models import KnowledgeDocument

def seed_all():
    print("Seeding CampusGPT LPU Database...")

    # 1. Test Student Account
    user, created = User.objects.get_or_create(
        username="12204567",
        defaults={
            "email": "student@lpu.in",
            "first_name": "Amit",
            "last_name": "Singh"
        }
    )
    if created:
        user.set_password("Student@123")
        user.save()
        StudentProfile.objects.create(
            user=user,
            reg_number="12204567",
            course="B.Tech Computer Science & Engineering",
            branch="CSE",
            semester=5,
            section="K22DF",
            phone="+91 9598993555",
            career_goal="Full Stack AI Engineer"
        )
        print("Created student user: 12204567 / Student@123")

    # 2. Faculty
    f1, _ = Faculty.objects.get_or_create(
        email="amar.cse@lpu.co.in",
        defaults={"name": "Dr. Amar Kumar", "department": "CSE", "phone": "9598993555", "office_room": "Block 34-402"}
    )
    f2, _ = Faculty.objects.get_or_create(
        email="javed.cse@lpu.co.in",
        defaults={"name": "Prof. Javed Sheikh", "department": "CSE", "phone": "9598993556", "office_room": "Block 34-508"}
    )
    f3, _ = Faculty.objects.get_or_create(
        email="jasmeet.math@lpu.co.in",
        defaults={"name": "Dr. Jasmeet Singh", "department": "Mathematics", "phone": "9598993557", "office_room": "Block 28-201"}
    )
    f4, _ = Faculty.objects.get_or_create(
        email="priya.ai@lpu.co.in",
        defaults={"name": "Dr. Priya Sharma", "department": "AI & Data Science", "phone": "9598993558", "office_room": "Block 35-304"}
    )

    # 3. Courses
    c_python, _ = Course.objects.get_or_create(code="CSE316", defaults={"name": "Operating Systems & Shell Scripting", "assigned_faculty": f1, "credits": 4})
    c_dsa, _ = Course.objects.get_or_create(code="CSE205", defaults={"name": "Data Structures and Algorithms", "assigned_faculty": f2, "credits": 4})
    c_ai, _ = Course.objects.get_or_create(code="INT404", defaults={"name": "Artificial Intelligence & Expert Systems", "assigned_faculty": f4, "credits": 4})
    c_math, _ = Course.objects.get_or_create(code="MTH401", defaults={"name": "Discrete Mathematics & Optimization", "assigned_faculty": f3, "credits": 3})
    c_web, _ = Course.objects.get_or_create(code="CSE326", defaults={"name": "Mobile & Cloud Applications", "assigned_faculty": f1, "credits": 3})

    # 4. Class Timetable
    timetable_samples = [
        (c_python, 'MON', time(9, 0), time(10, 0), '34-402'),
        (c_dsa, 'MON', time(10, 15), time(11, 15), '34-508'),
        (c_ai, 'MON', time(12, 0), time(13, 0), '35-304'),
        (c_math, 'TUE', time(9, 0), time(10, 0), '28-201'),
        (c_web, 'TUE', time(11, 0), time(13, 0), '34-LAB3'),
        (c_python, 'WED', time(10, 0), time(11, 0), '34-402'),
        (c_dsa, 'WED', time(14, 0), time(16, 0), '34-LAB1'),
        (c_ai, 'THU', time(9, 0), time(10, 0), '35-304'),
        (c_math, 'THU', time(11, 0), time(12, 0), '28-201'),
        (c_web, 'FRI', time(10, 0), time(11, 0), '34-402'),
        (c_dsa, 'FRI', time(11, 15), time(12, 15), '34-508'),
        (c_python, 'FRI', time(14, 0), time(15, 0), '27-407'),
    ]
    for course, day, start, end, room in timetable_samples:
        ClassTimetable.objects.get_or_create(
            course=course,
            day_of_week=day,
            start_time=start,
            end_time=end,
            defaults={"room_number": room, "section": "K22DF"}
        )

    # 5. Exam Schedules
    ExamSchedule.objects.get_or_create(
        course=c_dsa,
        exam_date=date.today() + timedelta(days=12),
        defaults={"start_time": time(10, 0), "end_time": time(12, 0), "room_number": "34-601", "exam_type": "Mid-Term (CA)"}
    )
    ExamSchedule.objects.get_or_create(
        course=c_python,
        exam_date=date.today() + timedelta(days=15),
        defaults={"start_time": time(14, 0), "end_time": time(16, 0), "room_number": "27-302", "exam_type": "Mid-Term (CA)"}
    )

    # 6. Subject Attendance
    attendance_data = [
        ("Data Structures and Algorithms", "CSE205", 32, 28, "Prof. Javed Sheikh"),
        ("Operating Systems", "CSE316", 30, 24, "Dr. Amar Kumar"),
        ("Artificial Intelligence", "INT404", 28, 25, "Dr. Priya Sharma"),
        ("Discrete Mathematics", "MTH401", 26, 18, "Dr. Jasmeet Singh"),  # Critical (<75%)
        ("Mobile & Cloud Applications", "CSE326", 24, 21, "Dr. Amar Kumar"),
    ]
    for name, code, total, attended, faculty_name in attendance_data:
        SubjectAttendance.objects.get_or_create(
            subject_code=code,
            defaults={
                "subject_name": name,
                "total_classes": total,
                "classes_attended": attended,
                "target_percentage": 75.0,
                "faculty_name": faculty_name
            }
        )

    # 7. Campus Verified Locations
    locations = [
        {
            "name": "Block 34 - Computer Science & IT Hub",
            "category": "academic",
            "block_number": "Block 34",
            "floor_or_room": "Floors 1-6, Labs 1-8",
            "latitude": 31.2555,
            "longitude": 75.7042,
            "description": "Primary academic building for CSE and IT departments. Features high-performance computing labs, project incubators, and faculty chambers.",
            "qr_code_id": "LPU-BLK34-CSE",
            "is_popular": True
        },
        {
            "name": "Block 37 & 38 - Central Library",
            "category": "library",
            "block_number": "Block 38",
            "floor_or_room": "Central Wing",
            "latitude": 31.2562,
            "longitude": 75.7050,
            "description": "4-storey modern central library with over 1.5M physical books, 24/7 exam reading halls, digital repository kiosks, and discussion pods.",
            "qr_code_id": "LPU-LIB-MAIN",
            "is_popular": True
        },
        {
            "name": "Baldev Raj Mittal Unipolis",
            "category": "sports",
            "block_number": "Unipolis",
            "floor_or_room": "Open Amphitheater",
            "latitude": 31.2549,
            "longitude": 75.7065,
            "description": "Massive open-air amphitheater with capacity exceeding 10,000 students. Venue for Youth Vibe, One India, celebrity concerts, and national hackathons.",
            "qr_code_id": "LPU-UNIPOLIS-MAIN",
            "is_popular": True
        },
        {
            "name": "UniMall Complex & Food Court",
            "category": "cafeteria",
            "block_number": "UniMall",
            "floor_or_room": "Ground & Upper Floors",
            "latitude": 31.2522,
            "longitude": 75.7048,
            "description": "Multi-storey commercial hub with Dominos, Subway, CCD, stationery shops, electronics repair, department store, and salon.",
            "qr_code_id": "LPU-UNIMALL",
            "is_popular": True
        },
        {
            "name": "Block 32 - Career Services & Admissions",
            "category": "office",
            "block_number": "Block 32",
            "floor_or_room": "Ground & First Floor",
            "latitude": 31.2538,
            "longitude": 75.7031,
            "description": "Houses the Division of Career Services (Placement Cell), International Student Affairs, and Central Admissions Counseling.",
            "qr_code_id": "LPU-BLK32-CAREER",
            "is_popular": True
        },
        {
            "name": "Block 27 - Mechanical & Robotics Labs",
            "category": "lab",
            "block_number": "Block 27",
            "floor_or_room": "Floors 1-4",
            "latitude": 31.2545,
            "longitude": 75.7020,
            "description": "School of Mechanical and Mechatronics Engineering. Houses CNC machinery, 3D printing lab, and autonomous vehicle project centers.",
            "qr_code_id": "LPU-BLK27-ENG",
            "is_popular": False
        },
        {
            "name": "UniHospital - 24/7 Healthcare Center",
            "category": "office",
            "block_number": "Main Gate Medical Hub",
            "floor_or_room": "Complete Facility",
            "latitude": 31.2518,
            "longitude": 75.7055,
            "description": "24/7 emergency and multispecialty healthcare for university residents. Free checkups, ambulance service, in-house pharmacy, and dental OPD.",
            "qr_code_id": "LPU-HOSPITAL",
            "is_popular": True
        },
        {
            "name": "Boys Hostel Complex (BH-1 to BH-8)",
            "category": "hostel",
            "block_number": "Residential Zone North",
            "floor_or_room": "Apartments & Common Mess",
            "latitude": 31.2580,
            "longitude": 75.7070,
            "description": "Modern residential hostels with study rooms, high-speed Wi-Fi, indoor games, basketball courts, and dining halls.",
            "qr_code_id": "LPU-HOSTEL-BH",
            "is_popular": False
        }
    ]
    for loc in locations:
        CampusLocation.objects.get_or_create(qr_code_id=loc['qr_code_id'], defaults=loc)

    # 8. Campus Events
    events_data = [
        {
            "title": "HackLPU 2026 – 36hr National Hackathon",
            "category": "hackathon",
            "description": "Flagship annual 36-hour hackathon with cash prizes over Rs 5,00,000. Tracks include Generative AI, Web3, Smart Cities, and Healthcare.",
            "venue": "Baldev Raj Mittal Unipolis",
            "organizer": "Google Developer Student Club & Coding Oasis",
            "start_date": timezone.now() + timedelta(days=5),
            "end_date": timezone.now() + timedelta(days=7),
            "registration_url": "https://hacklpu2026.devpost.com",
            "is_featured": True,
            "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600"
        },
        {
            "title": "Generative AI & Agentic Systems Workshop",
            "category": "workshop",
            "description": "Hands-on deep dive into Google Gemini 1.5, RAG pipelines, and multi-agent systems with industry engineers from Google Cloud.",
            "venue": "Block 34, 4th Floor Audi",
            "organizer": "Division of Student Affairs & CSE Dept",
            "start_date": timezone.now() + timedelta(days=8),
            "end_date": timezone.now() + timedelta(days=8, hours=4),
            "registration_url": "https://ums.lpu.in/workshops",
            "is_featured": True,
            "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600"
        },
        {
            "title": "Microsoft & Tier-1 Placement Drive Briefing",
            "category": "placement",
            "description": "Essential placement readiness session outlining eligibility thresholds, online coding rounds, system design expectations, and interview etiquette.",
            "venue": "Shanti Devi Mittal Auditorium",
            "organizer": "Division of Career Services",
            "start_date": timezone.now() + timedelta(days=11),
            "end_date": timezone.now() + timedelta(days=11, hours=3),
            "registration_url": "https://ums.lpu.in/placement",
            "is_featured": True,
            "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600"
        },
        {
            "title": "Youth Vibe 2026 – Annual Cultural Extravaganza",
            "category": "cultural",
            "description": "One of India's largest university festivals with 50+ competitions in music, dance, theater, fashion, gaming, and celebrity night performances.",
            "venue": "Entire Campus & Unipolis Arena",
            "organizer": "Department of Cultural Affairs",
            "start_date": timezone.now() + timedelta(days=22),
            "end_date": timezone.now() + timedelta(days=26),
            "registration_url": "https://youthvibe.lpu.in",
            "is_featured": False,
            "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600"
        }
    ]
    for ev in events_data:
        CampusEvent.objects.get_or_create(title=ev['title'], defaults=ev)

    # 9. Lost & Found Items
    lost_found_samples = [
        {
            "title": "HP Pavilion Blue Laptop Charger (65W)",
            "item_type": "lost",
            "category": "electronics",
            "description": "Left behind in Block 34 Lab 402 on table near the whiteboard. Has an identifiable orange electrical tape wrapped around the cable connector.",
            "location_name": "Block 34, Lab 402",
            "contact_phone": "+91 9876543210",
            "reporter_name": "Rohan Sharma"
        },
        {
            "title": "Black Noise ColorFit Smartwatch",
            "item_type": "found",
            "category": "accessories",
            "description": "Found on the 2nd floor reading hall couch in Central Library Block 38. Has a black silicone strap and small scratch on the bottom bezel.",
            "location_name": "Central Library (Block 38)",
            "contact_phone": "+91 9876543211",
            "reporter_name": "Library Security Desk"
        },
        {
            "title": "LPU Student ID Card (Reg No: 12109843)",
            "item_type": "found",
            "category": "id_cards",
            "description": "Found near UniMall Domino's order counter. Student name printed: Vikram Patel, Department of Mechanical Engineering.",
            "location_name": "UniMall Ground Floor",
            "contact_phone": "+91 9876543212",
            "reporter_name": "UniMall Helpdesk"
        }
    ]
    for it in lost_found_samples:
        LostFoundItem.objects.get_or_create(title=it['title'], defaults=it)

    # 10. Interview Questions
    interview_samples = [
        {
            "question_type": "technical",
            "role_category": "Software Engineering",
            "question": "Explain the difference between Processes and Threads, and how context switching behaves in an OS.",
            "sample_answer": "A process is an executing instance of a program with its own dedicated memory address space, file descriptors, and security context. A thread is a lightweight unit of execution within a process that shares the parent process's memory heap, code, and global variables while maintaining its own stack and registers. Context switching between threads within the same process is significantly faster than between processes because virtual memory pages and TLB caches do not need invalidation.",
            "tips": "Always mention memory sharing, TLB flush overhead, and concurrency vs parallelism.",
            "difficulty": "Medium"
        },
        {
            "question_type": "dsa",
            "role_category": "Algorithms",
            "question": "How do you detect a cycle in a Directed Graph vs an Undirected Graph?",
            "sample_answer": "For an Undirected Graph, cycle detection can be accomplished using DFS with a visited set and a parent pointer (or Disjoint Set Union). If an adjacent vertex is already visited and not the parent, a cycle exists. For a Directed Graph, simple visited checking is insufficient; you must track vertices in the current recursive call stack (DFS with 3 colors: unvisited, currently visiting, and fully processed) or use Kahn's Algorithm (topological sort with in-degrees).",
            "tips": "Draw the difference between a back edge and a cross edge.",
            "difficulty": "Hard"
        },
        {
            "question_type": "hr",
            "role_category": "Behavioral",
            "question": "Tell me about a situation where a group project encountered a severe conflict or roadblock. How did you handle it?",
            "sample_answer": "Structure response using STAR: Situation (describe the group task at LPU), Task (your deliverable deadline), Action (how you initiated objective discussion, identified bottleneck, and reallocated tasks according to each member's strength), Result (delivered project on schedule with A grade).",
            "tips": "Focus on empathy, active listening, and objective resolution rather than blaming teammates.",
            "difficulty": "Easy"
        }
    ]
    for q in interview_samples:
        InterviewQuestion.objects.get_or_create(question=q['question'], defaults=q)

    # 11. Initial Notifications
    notifs = [
        ("Upcoming Class: Operating Systems", "Your next class (CSE316) starts at 09:00 AM in Room 34-402 with Dr. Amar Kumar.", "class"),
        ("Attendance Warning: Discrete Mathematics", "Your attendance in MTH401 is 69.2% (below required 75%). Attend the next 5 classes to reach safety.", "attendance"),
        ("HackLPU 2026 Registration Open", "Registrations for HackLPU are now live on Devpost. Rs 5,00,000 in prizes. Click to register.", "event"),
        ("Mid-Term Exam Datesheet Announced", "The continuous assessment midterm datesheet has been published on UMS portal.", "exam"),
    ]
    for title, msg, n_type in notifs:
        Notification.objects.get_or_create(title=title, defaults={"message": msg, "notification_type": n_type, "user": user})

    print("Successfully seeded all LPU sample data!")

if __name__ == '__main__':
    seed_all()
