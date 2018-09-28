const words = [
    "pickle",
    "baby",
    "computer",
    "chair",
    "book",
    "phone",
    "run",
    "jeans",
    "shirt",
    "dress",
    "code",
    "is",
    "hello",
    "world"
];

function randint(n) {
    return Math.floor(Math.random() * n);
}

function word() {
    return words[randint(words.length)];
}

exports.passwordGenerator = _ => {
    return `${word()} ${word()} ${word()} ${word()}`
}