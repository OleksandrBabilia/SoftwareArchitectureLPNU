import React, { useState } from 'react';
import BookItem from '../components/BookItem';
import useBooks from '../hooks/useBooks';
import '../styles/book/BookList.css';
import Navbar from '../components/Navbar';  // Import Navbar

const BookList = () => {
    const { books, authors, publishers, loading, error } = useBooks();

    const [selectedAuthors, setSelectedAuthors] = useState([]);
    const [selectedPublishers, setSelectedPublishers] = useState([]);
    const [sortOrder, setSortOrder] = useState('asc');
    const [sortBy, setSortBy] = useState('title');
    const [searchQuery, setSearchQuery] = useState('');
    const [showAvailableOnly, setShowAvailableOnly] = useState(false); // State for filtering rented books

    // Pagination state
    const [currentPage, setCurrentPage] = useState(1);
    const booksPerPage = 20;

    if (loading) {
        return <p className="text-center">Loading books...</p>;
    }

    if (error) {
        return <p className="text-center text-danger">{error}</p>;
    }

    if (!Object.keys(authors).length || !Object.keys(publishers).length) {
        return <p className="text-center">Loading authors and publishers...</p>;
    }

    const handleAuthorChange = (authorId) => {
        setSelectedAuthors((prevState) => {
            if (prevState.includes(authorId)) {
                return prevState.filter((id) => id !== authorId);
            } else {
                return [...prevState, authorId];
            }
        });
    };

    const handlePublisherChange = (publisherId) => {
        setSelectedPublishers((prevState) => {
            if (prevState.includes(publisherId)) {
                return prevState.filter((id) => id !== publisherId);
            } else {
                return [...prevState, publisherId];
            }
        });
    };

    const filteredBooks = books.filter((book) => {
        const matchesAuthor = selectedAuthors.length > 0
            ? book.author.some((authorId) => selectedAuthors.map(Number).includes(authorId))
            : true;

        const matchesPublisher = selectedPublishers.length > 0
            ? selectedPublishers.map(Number).includes(book.publisher)
            : true;

        const matchesSearch = searchQuery ? (
            book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            book.isbn.includes(searchQuery)
        ) : true;

        const matchesAvailability = showAvailableOnly ? !book.rented : true; // Filter by rented status if showAvailableOnly is true

        return matchesAuthor && matchesPublisher && matchesSearch && matchesAvailability;
    });

    const sortedBooks = filteredBooks.sort((a, b) => {
        let compareA, compareB;

        if (sortBy === 'title') {
            compareA = a.title.toLowerCase();
            compareB = b.title.toLowerCase();
        } else if (sortBy === 'isbn') {
            compareA = a.isbn;
            compareB = b.isbn;
        } else if (sortBy === 'author') {
            compareA = authors[a.author[0]].toLowerCase();
            compareB = authors[b.author[0]].toLowerCase();
        } else if (sortBy === 'publisher') {
            compareA = publishers[a.publisher].toLowerCase();
            compareB = publishers[b.publisher].toLowerCase();
        }

        if (sortOrder === 'asc') {
            return compareA < compareB ? -1 : compareA > compareB ? 1 : 0;
        } else {
            return compareA > compareB ? -1 : compareA < compareB ? 1 : 0;
        }
    });

    const handleSortOrderChange = (event) => {
        setSortOrder(event.target.value);
    };

    const handleSortByChange = (event) => {
        setSortBy(event.target.value);
    };

    const handleSearchQueryChange = (event) => {
        setSearchQuery(event.target.value);
    };

    // Pagination logic
    const totalPages = Math.ceil(sortedBooks.length / booksPerPage);
    const indexOfLastBook = currentPage * booksPerPage;
    const indexOfFirstBook = indexOfLastBook - booksPerPage;
    const currentBooks = sortedBooks.slice(indexOfFirstBook, indexOfLastBook);

    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    const paginationRange = () => {
        const pages = [];
        if (totalPages <= 7) {
            for (let i = 1; i <= totalPages; i++) {
                pages.push(i);
            }
        } else {
            pages.push(1);
            if (currentPage > 4) pages.push('...');
            for (let i = Math.max(2, currentPage - 1); i <= Math.min(currentPage + 1, totalPages - 1); i++) {
                pages.push(i);
            }
            if (currentPage < totalPages - 3) pages.push('...');
            pages.push(totalPages);
        }
        return pages;
    };

    return (
        <div className="container mt-4">
            <Navbar /> {/* Include Navbar here */}
            <h2 className="mb-4 text-center"> </h2>

            <div className="row">
                <div className="col-md-3 mb-4">
                    <div className="p-3 border rounded">
                        <h4>Filter Books</h4>
                        {/* Filter for available books */}


                        {/* Author and Publisher filters */}
                        <div className="mb-3">
                            <h5>Authors</h5>
                            <div className="scrollable-container">
                                {Object.keys(authors).map((authorId) => (
                                    <div key={authorId} className="form-check">
                                        <input
                                            className="form-check-input"
                                            type="checkbox"
                                            value={authorId}
                                            id={`author-${authorId}`}
                                            checked={selectedAuthors.includes(authorId)}
                                            onChange={() => handleAuthorChange(authorId)}
                                        />
                                        <label className="form-check-label" htmlFor={`author-${authorId}`}>
                                            {authors[authorId]}
                                        </label>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="mb-3">
                            <h5>Publishers</h5>
                            <div className="scrollable-container">
                                {Object.keys(publishers).map((publisherId) => (
                                    <div key={publisherId} className="form-check">
                                        <input
                                            className="form-check-input"
                                            type="checkbox"
                                            value={publisherId}
                                            id={`publisher-${publisherId}`}
                                            checked={selectedPublishers.includes(publisherId)}
                                            onChange={() => handlePublisherChange(publisherId)}
                                        />
                                        <label className="form-check-label" htmlFor={`publisher-${publisherId}`}>
                                            {publishers[publisherId]}
                                        </label>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                <div className="col-md-8">
                    {/* Search, Sort, and Pagination controls */}
                    <div className="d-flex justify-content-end align-items-center mb-3">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Search books..."
                            value={searchQuery}
                            onChange={handleSearchQueryChange}
                            aria-label="Search"
                        />
                        <button
                            className="btn-custom ml-3"
                            onClick={() => setSearchQuery(searchQuery)}
                        >
                            Search
                        </button>

                        <select
                            className="form-select w-auto ml-3"
                            value={sortBy}
                            onChange={handleSortByChange}
                            aria-label="Sort by"
                        >
                            <option value="title">Sort by Name</option>
                            <option value="isbn">Sort by ISBN</option>
                            <option value="author">Sort by Author Name</option>
                            <option value="publisher">Sort by Publisher Name</option>
                        </select>

                        <select
                            className="form-select w-auto ml-3"
                            value={sortOrder}
                            onChange={handleSortOrderChange}
                            aria-label="Sort order"
                        >
                            <option value="asc">Ascending</option>
                            <option value="desc">Descending</option>
                        </select>
                    </div>

                    <div className="row">
                        {currentBooks.length > 0 ? (
                            currentBooks.map((book) => (
                                <BookItem key={book.id} book={book} author={authors} publisher={publishers} />
                            ))
                        ) : (
                            <p className="text-center">No books found matching your criteria.</p>
                        )}
                    </div>

                    {/* Pagination */}
                    <div className="d-flex justify-content-center mt-4">
                        {paginationRange().map((page, index) => (
                            page === '...' ? (
                                <button key={index} className="btn-custom disabled">...</button>
                            ) : (
                                <button
                                    key={index}
                                    className={`btn-custom ${currentPage === page ? 'active' : ''}`}
                                    onClick={() => handlePageChange(page)}
                                >
                                    {page}
                                </button>
                            )
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BookList;
