let bookings = [];

function bookAppointment() {
  const parentName = document.getElementById('parent-name').value;
  const studentName = document.getElementById('student-name').value;
  const date = document.getElementById('date').value;
  const time = document.getElementById('time').value;

  const newBooking = {
    parentName,
    studentName,
    date,
    time,
  };

  bookings.push(newBooking);

  document.getElementById('booking-details').textContent = JSON.stringify(
    bookings,
    null,
    2
  );

  // Reset the form
  document.getElementById('booking-form').reset();
}
