# API Response Defintion

This file describes how the information parsed from an analyzed document will be returned by our API. Information will be returned in JSON form. For reference see an abbreviated example [located here](ProgLang-PA1.json).

- `DocumentID` - Document Data Store ID of the source document.
- `URL` - The url of the source document.
- `AsOfDate` - The date the information associated with this response was passed to analysis engine.
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
- `NGrams` - List of objects desrcibing different n-grams found in the srouce document. Includes entries for `n = 2` and `n = 3` by default.
    - `N` - Value of `n` for this list of n-grams.
    - `Grams` - List of objects with frequency and positional information for each n-gram in the document for above `n`. Entries are sorted first in order of descending frequency then in alphabetic order.
        - `Text` - The actual text of the n-gram described by this object.
        - `Count` - The number of times this n-gram appeared in the document.
        - `Occurences` - List of locations within the document where this n-gram occurs in the document. Number indicates the position of the first token of the n-gram. 1 indicates this n-gram starts at the first token in the document. This list is `Count` long.
    