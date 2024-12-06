// helpers/genreHelper.js

const GANRES_IDS = {
    1: "Fiction",
    2: "Nonfiction",
    3: "Science Fiction",
    4: "Mystery",
    5: "Romance",
    6: "History",
    7: "Biography"
};

export function getGenreName(genreId) {
    return GANRES_IDS[genreId] || "Unknown Genre";
}
