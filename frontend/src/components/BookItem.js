import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getGenreName } from '../helpers/genreHelper';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { Modal, Button } from 'react-bootstrap';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import './BookItem.css';

const BookItem = ({ book, author, publisher }) => {
  const navigate = useNavigate();
  const [isRented, setIsRented] = useState(book.rented);
  const [showModal, setShowModal] = useState(false);
  const [rentalDate, setRentalDate] = useState(new Date());
  const [returnDate, setReturnDate] = useState(new Date());

  const handleRentBook = async () => {
    const rentalData = {
      rental_date: rentalDate.toISOString(),
      return_date: returnDate.toISOString(),
    };

    const token = localStorage.getItem('token');
    if (!token) {
      toast.error('You are not logged in. Please log in first.', {
        position: 'top-center',
      });
      navigate('/login');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/books/${book.id}/rent/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(rentalData),
      });

      if (response.ok) {
        setIsRented(true);
        toast.success('Book rented successfully!', {
          position: 'top-center',
        });
      } else {
        toast.error('Failed to rent the book. Please try again.', {
          position: 'top-center',
        });
      }
    } catch (error) {
      console.error('Error occurred while renting the book:', error);
      toast.error('An error occurred. Please try again later.', {
        position: 'top-center',
      });
    }
  };

  return (
      <div className="col-md-3 mb-4">
        <div className="card book-card h-100 shadow-lg rounded">
          <img
              src={book.cover || '/default_book_image.jpg'}
              className="card-img-top book-img"
              alt={`${book.title} cover`}
          />
          <div className="card-body">
            <h5 className="card-title text-white">{book.title}</h5>
            <p className="card-text text-light">
              <strong>ISBN:</strong> {book.isbn}
            </p>
            <p className="card-text text-light">
              <strong>Rented:</strong> {book.rented ? 'Yes' : 'No'}
            </p>
            <p className="card-text text-light">
              <strong>Author(s):</strong> {book.author
                .map((authorId) => author[authorId] || 'Unknown Author')
                .join(', ')}
            </p>
            <p className="card-text text-light">
              <strong>Publisher:</strong> {publisher[book.publisher] || 'Unknown Publisher'}
            </p>
            <p className="card-text text-light">
              <strong>Genres:</strong> {getGenreName(book.ganres)}
            </p>

            {!isRented ? (
                <p className="availability-status available">
                  <span className="icon">✔️</span> Available
                </p>
            ) : (
                <p className="availability-status not-available">
                  <span className="icon">❌</span> Not Available
                </p>
            )}

            {!isRented && (
                <button onClick={() => setShowModal(true)} className="btn btn-custom w-100">
                  Rent this Book
                </button>
            )}
          </div>
        </div>

        <Modal show={showModal} onHide={() => setShowModal(false)} className="custom-modal">
          <Modal.Header closeButton>
            <Modal.Title>Pick Rental and Return Dates</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div className="mb-3">
              <label htmlFor="rental-date" className="form-label">Rental Date</label>
              <DatePicker
                  selected={rentalDate}
                  onChange={date => setRentalDate(date)}
                  showTimeSelect
                  dateFormat="Pp"
                  id="rental-date"
                  className="form-control"
              />
            </div>

            <div className="mb-3">
              <label htmlFor="return-date" className="form-label">Return Date</label>
              <DatePicker
                  selected={returnDate}
                  onChange={date => setReturnDate(date)}
                  showTimeSelect
                  dateFormat="Pp"
                  id="return-date"
                  className="form-control"
              />
            </div>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Close
            </Button>
            <Button variant="primary" onClick={() => {
              handleRentBook();
              setShowModal(false);
            }}>
              Rent this Book
            </Button>
          </Modal.Footer>
        </Modal>

        {/* Toast Container */}
        <ToastContainer />
      </div>
  );
};

export default BookItem;
