# API Response Defintion

This file describes how the information parsed from an analyzed document will be returned by our API. Information will be returned in JSON form. For reference see an abbreviated example [located here](ProgLang-PA1.json).

- `URL` - The url of the source document.
- `AsOfDate` - The date the information associated with this response was passed to - analysis engine.
- `Meta` - Object describing high level summary information about the document.
    - `Title` - Inferred document title.
    - `Author` - Inferred document author.
    - `DateCreated` - Date the document was first published.
    - `DateModified` - The most recent date the document was modified. If the document was never modified this will be the same as DateCreated.
    - `Keywords` - List of phrases (not guarenteed to be single words) deemed to be highly important.
- `Words` - Object that contains distribution of words in the document.
    - `NumWords` - The total number of words in the document.
    - `NumDistinctWords` - The total number of distinct words in the document.
    - `WordCounts` - List of objects with frequency and positional information for each distinct word in the document. This list is `NumDistinctWords` long. Entries are sorted first in order of descending frequency then in alphabetic order.
        - `Text` - The word described by this object.
        - `Count` - The number of times this word appeared in the document. The sum of all `Count` attributes within the `WordCounts` list will equal `NumWords`.
        - `Occurences` - List of locations within the document where this word occured in the document. 1 indicates this is the first token in the document. This list is `Count` long.
- `NGrams` - List of bigrams and trigrams that appear in the document.
    - `BiGrams` - List of objects with frequency and positional information for each bigram in the document. Entries are sorted first in order of descending frequency then in alphabetic order.
        - `Text` - The actual text of the bigram described by this object.
        - `Count` - The number of times this bigram appeared in the document.
        - `Occurences` - List of locations within the document where this bigram occurs in the document. Number indicates the position of the first token of the bigram. 1 indicates this bigram starts at the first token in the document. This list is `Count` long.
    - `TriGrams` - List of objects with frequency and positional information for each trigram in the document.
        - `Text` - The actual text of the trigram described by this object.
        - `Count` - The number of times this trigram appeared in the document.
        - `Occurences` - List of locations within the document where this trigram occurs in the document. Number indicates the position of the first token of the trigram. 1 indicates this trigram starts at the first token in the document. This list is `Count` long.