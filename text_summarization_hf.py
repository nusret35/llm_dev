from transformers import pipeline
import textwrap
import re

def format_text(text):
    # Split the text into sentences
    sentences = re.split('\.\s*', text)
    
    # Capitalize the first letter of each sentence and join them back together
    sentences = [s.strip().capitalize() for s in sentences if s]
    formatted_text = '. '.join(sentences) + '.'
    
    return formatted_text

# Loading summarization pipeline
summarizer = pipeline('summarization')

# Summarizing text
syllabus = """
Course Meeting Times
Lectures: 2 sessions / week, 1 hour / session

Recitations: 2 sessions / week, 1 hour / session

Tutorials: 1 session / week, 1 hour / session

Prerequisites
6.004 Computation Structures and 6.005 Software Construction or 6.009 Fundamentals of Programming

Learning Objectives
After completing this class, the students will be able to design their own distributed systems to solve real-world problems. The ability to design one’s own distributed system includes an ability to argue for one’s design choices.

This primary objective is supported by a few others:

The students will be able to evaluate and critique existing systems, as well as their own system designs. As part of that, students will learn to recognize design choices made in existing systems.
The students will be able to apply the technical material taught in lecture to new system components. This implies an ability to recognize and describe:
How common design patterns in computer system—such as abstraction and modularity—are used to limit complexity.
How operating systems use virtualization and abstraction to enforce modularity.
How the Internet is designed to deal with scale, a diversity of applications, and competing economic interests.
How reliable, usable distributed systems are able to be built on top of an unreliable network.
Common pitfalls in the security of computer systems, and how to combat them.
Because this is a Communication Intensive in the Major (CI-M) class, students will also learn to communicate in forms that are common in the field of computer systems. This includes written design reports, oral presentations, and peer review.

The communication instruction also supports the primary learning objective of designing systems. In the real world, we design systems in teams, and communication of many forms (written, oral, etc.) is part of that process.

Required Text
Saltzer, Jerome H. and M. Frans Kaashoek. Principles of Computer System Design: An Introduction, Part I. Morgan Kaufmann, 2009. ISBN: 9780123749574. [Preview with Google Books]

The text supplements the lectures and recitations; it should be your first resource when you are confused by a lecture topic, or want more information.

Part II of the textbook is available on MIT OpenCourseWare.

Course Structure
The course has three components: lectures, recitations, and tutorials. We expect you to attend all three, as they each serve a different purpose.

1. Lectures

Lectures are held on Mondays and Wednesdays for one hour. The lectures are designed to teach students the technical details necessary to design their own systems and to put those details in larger contexts: both the contexts of a specific area of systems as well as systems in general.

This type of material appears in lectures because that’s what lectures are good at: giving a higher-level context for the details of the class.

2. Recitations

Recitations are held on Tuesdays and Thursdays for one hour. For the first recitation, attend whichever one you want. After that, you will be assigned a permanent section.

Recitations are designed to give students a chance to practice their system-analysis and oral communication skills. Each recitation revolves around a particular paper in systems. Through reading these papers, students get a better sense of how communication in the field is done. Recitations are discussion-based; students get practice analyzing, critiquing, and communicating about systems.

3. Writing Tutorials

Writing tutorials are held on Fridays for one hour. We will assign your time slot during the first week of classes.

Most of these tutorials will teach the communication theory and practices of this course and assist you in preparing for the assignments. You’ll become fluent in a variety of communication genres, develop strategies and skills needed to present technical concepts to different audiences, learn how to use writing to develop and deepen your technical understanding—and get specific, directed instruction on writing and presenting your assignments. A handful of the tutorials will be dedicated to discussing the design project.

Late Policy
You must hand in assignments when they are due, and you must attend quizzes at the scheduled times. If you feel you have a compelling reason for not handing in an assignment on time, or for not attending a quiz, please talk to Dr. LaCurts in advance.

The only exception to this late policy is design project materials. For those, the late policy will be explicitly posted on each assignment.

If you miss an assignment deadline, you should still hand in the assignment; we’ll give you feedback even though we won’t give you credit for your final grade. Furthermore, doing assignments is the best way to prepare for exams and design project. Unless otherwise specified, assignments are due at 5:00pm on their assigned due-date.

Grade Components
Each assignment supports the objectives of the class in various ways.

Technical Material (35% of Grade)
Quizzes: One quiz is held during the term. A second quiz will be scheduled during finals week. Each quiz will focus on half of the class material, but keep in mind that later topics build heavily upon the earlier topics. The quizzes will test material from lectures, recitations, and the assigned reading and let us test whether students have mastered the technical material.
Hands-ons: During most weeks, you will be expected to complete a hands-on experiment that requires a computer. These reinforce some of the abstract concepts from the lectures or papers that week and let you find out how things really work. (Note: Hands-on experiments are not available to OCW users.)
Communication + System Design and Analysis (40% of Grade)
The staff has worked with the MIT Writing, Rhetoric, and Professional Communication (WRAP) program for more than 10 years to design the writing and speaking assignments. We have chosen assignments that are similar to the kinds of writing you will do in the engineering workplace: Preliminary reports, final reports, and presentations. Communication assignments are designed to help you conceptualize and develop the design project.

Design Project: The primary assignment in 6.033 is the design project (DP). This project is where the students get to design their own system, which is the primary objective of this course.
The DP requires you to develop a detailed system design to solve a real-world problem. This project will extend over most of the semester, and will be done in teams of three students, all of whom attend the same writing tutorial (with exceptions only for extenuating circumstances). Real-world systems are not built individually; it’s always a team effort. Part of the DP is to learn to work productively and effectively in this setting. We will give you tools for doing so in the writing tutorials.

The DP consists of multiple deliverables: a preliminary report, oral presentation, final report, and peer review. The Design Project page gives more detail about the DP deliverables.

System Critiques: One of the goals of this class is for students to be able to analyze and critique technical systems. We will assign multiple system critiques during the semester.
These critiques will be graded by your Teaching Assistants (TAs) and/or Communication Instructors and assigned a letter grade (we will specify more details about grading in each of the assignments). The expectations for each individual critique will be detailed in the tutorials. As your skills at analyzing and reading technical papers improve throughout the semester, we will expect your critiques to reflect that.

Participation (25% of Grade)
Recitation Participation: Our recitations are discussion-based, and we expect you to be engaged and participate. Participating in a recitation means:
Coming prepared to recitation (doing the reading, turning in the pre-reading question etc.)
Paying attention when the instructor is speaking (you can’t participation in a discussion if you don’t know what it’s about)
Participating (verbally) in pair-/group-work
Volunteering to answer questions when the instructor asks them. (Note that you may not get called on each time. That’s okay; our class sizes prevent that. Statistically, if you’re raising your hand frequently, you’ll get called on with some frequency.)
Responding to other student’s comments with an opinion of their own.
Asking good questions in recitation (where “good” just means it’s clear that you prepared for the recitation).
We will assign the participation grade in two parts: one for the first half of the semester, one for the second half of the semester. We will also give you preliminary grades for each of these (one about a quarter into the semester, one about three quarters into the semester), so that you know where you stand and have time to improve. This document explains in more detail how your participation grade is determined.

Communication Participation: A portion of your participation grade will also be based on your participation in writing tutorials and on your understanding of communication concepts and skills, as demonstrated by your work on the design project and evaluated by your communication instructor.

Note that over a third of your grade comes from written assignments; we expect you to take writing seriously in this class.

Grading
The class consists of three components: technical material, communication/system design and analysis, and participation. Each of these components comprises roughly one third of your grade, according to the following breakdown:

ACTIVITIES	PERCENTAGES
Technical Material 30% for Quizzes (two @ 15% each) 5% for Hands-Ons	35%
Communication + System Design and Analysis 10% for Design Project (DP) Preliminary Report and Presentation
20% for DP report

4% for DP Peer Review

6% for Critiques (Critique #1 =2%, Critique #2 = 4%)

40%
Participation 20% for Recitation Participation
5% for Communication Participation

25%
You must complete all design project assignments in order to pass 6.033. If you do not, you will automatically receive an F.

Collaboration Policy
You may not collaborate on quizzes. On hands-ons, it’s okay to discuss ideas with your classmates, but you should not be collaborating on the actual answers. Take the UNIX hands-on for example: it’s okay to talk to your classmates about what pipes are, it’s not okay to work together to come up with a command that gives a long listing of the smallest given files in the /etc directory whose name contains the string “.conf”, sorted by increasing file size (i.e., the solution to one of the first questions).

On all writing assignments you are welcome to discuss ideas with others, but your writing should be your own and you should acknowledge all contributions of ideas by others, whether from classmates or from papers you have read.
"""

# Split the text into chunks of approximately 1024 words each.
# Adjust the word count if your text uses particularly long or short words on average
chunks = textwrap.wrap(syllabus, 1024)

# Initialize an empty string to store the summaries
summary = ""

# Summarize each chunk
for chunk in chunks:
    summarized_chunk = summarizer(chunk, max_length=50, min_length=30, do_sample=False)
    # Each summarized_chunk is a list with a dictionary {'summary_text': '...'} so we get the 'summary_text'
    summary += summarized_chunk[0]['summary_text']

# Format the summarized text
formatted_summary = format_text(summary)

# Print the formatted summary
print(formatted_summary)
