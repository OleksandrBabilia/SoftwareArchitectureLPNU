// src/hooks/useBooks.js

import { useState, useEffect } from 'react';
import axios from 'axios';

const useBooks = () => {
  const [books, setBooks] = useState([]);
  const [authors, setAuthors] = useState({});
  const [publishers, setPublishers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/books/');
        console.log('Books:', response.data); // Log books
        setBooks(response.data);
        await fetchAuthors(response.data); // Fetch authors for each book
        await fetchPublishers(response.data); // Fetch publishers for each book
        setLoading(false); // Set loading to false after all fetches complete
      } catch (err) {
        setError('Error fetching books');
        setLoading(false);
      }
    };

    const fetchAuthors = async (books) => {
      const authorIds = new Set();
      books.forEach((book) => {
        book.author.forEach((author) => {
          authorIds.add(author); // Collect author IDs
        });
      });

      try {
        const authorPromises = [...authorIds].map((authorId) =>
            axios.get(`http://127.0.0.1:8000/api/v1/authors/${authorId}/`)
        );
        const authorResponses = await Promise.all(authorPromises);
        const authorData = authorResponses.reduce((acc, response) => {
          const { id, first_name, last_name } = response.data;
          acc[id] = `${first_name} ${last_name}`;
          return acc;
        }, {});
        console.log('Authors:', authorData); // Log authors
        setAuthors(authorData); // Store author data
      } catch (err) {
        setError('Error fetching author details');
      }
    };

    const fetchPublishers = async (books) => {
      const publisherIds = new Set();
      books.forEach((book) => {
        publisherIds.add(book.publisher); // Collect publisher IDs
      });

      try {
        const publisherPromises = [...publisherIds].map((publisherID) =>
            axios.get(`http://127.0.0.1:8000/api/v1/publishers/${publisherID}/`)
        );
        const publisherResponses = await Promise.all(publisherPromises);
        const publisherData = publisherResponses.reduce((acc, response) => {
          const { id, name } = response.data;
          acc[id] = name;
          return acc;
        }, {});
        console.log('Publishers:', publisherData); // Log publishers
        setPublishers(publisherData); // Store publisher data
      } catch (err) {
        setError('Error fetching publisher details');
      }
    };

    fetchBooks();
  }, []);

  return { books, authors, publishers, loading, error };
};

export default useBooks;
