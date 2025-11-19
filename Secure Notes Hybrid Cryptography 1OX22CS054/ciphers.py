# ciphers.py
# Implements Caesar -> Vigenere -> Playfair pipeline (and reverse).
# Designed to keep non-alpha characters in original positions (they are recorded and reinserted).
# Also records where 'J' originally occurred (Playfair merges I/J).

import string

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ---------------------------
# Helpers: normalization
# ---------------------------
def _record_non_alpha_and_letters(text):
    """Return (letters_only_upper, non_alpha_positions, j_positions, original_length).
       letters_only_upper has J replaced by I (Playfair convention).
       non_alpha_positions: list of (index, char) in original text.
       j_positions: indices (in letters_only) where original char was J/j.
    """
    non_alpha_positions = []
    letters = []
    j_positions = []
    for idx, ch in enumerate(text):
        if ch.isalpha():
            up = ch.upper()
            if up == 'J':
                j_positions.append(len(letters))
                up = 'I'
            letters.append(up)
        else:
            non_alpha_positions.append((idx, ch))
    return ''.join(letters), non_alpha_positions, j_positions, len(text)

def _reinsert_non_alpha(original_length, letters_only, non_alpha_positions, j_positions):
    """Reconstruct full text of length original_length by inserting non-alpha chars at positions.
       j_positions: indices within letters_only which should be restored to 'J'.
    """
    # Convert letters_only into list and restore J's
    letters_list = list(letters_only)
    for pos in j_positions:
        if 0 <= pos < len(letters_list):
            letters_list[pos] = 'J'

    out = [None] * original_length
    # place non-alpha
    for idx, ch in non_alpha_positions:
        out[idx] = ch

    # place letters in remaining slots left-to-right
    li = 0
    for i in range(original_length):
        if out[i] is None:
            if li < len(letters_list):
                out[i] = letters_list[li]
                li += 1
            else:
                out[i] = ''  # safety
    return ''.join(out)

# ---------------------------
# Caesar
# ---------------------------
def caesar_encrypt_letters(letters, shift):
    shift = shift % 26
    out = []
    for ch in letters:
        if ch in ALPHA:
            out.append(ALPHA[(ALPHA.index(ch) + shift) % 26])
        else:
            out.append(ch)
    return ''.join(out)

def caesar_decrypt_letters(letters, shift):
    return caesar_encrypt_letters(letters, -shift)

# ---------------------------
# Vigenere
# ---------------------------
def _extend_key(key, length):
    key = ''.join([c for c in key.upper() if c.isalpha()])
    if not key:
        raise ValueError("Vigenere key must contain letters")
    times = (length + len(key) - 1) // len(key)
    return (key * times)[:length]

def vigenere_encrypt_letters(letters, key):
    if not letters:
        return ''
    key_stream = _extend_key(key, len(letters))
    out = []
    for p, k in zip(letters, key_stream):
        out.append(ALPHA[(ALPHA.index(p) + ALPHA.index(k)) % 26])
    return ''.join(out)

def vigenere_decrypt_letters(letters, key):
    if not letters:
        return ''
    key_stream = _extend_key(key, len(letters))
    out = []
    for c, k in zip(letters, key_stream):
        out.append(ALPHA[(ALPHA.index(c) - ALPHA.index(k)) % 26])
    return ''.join(out)

# ---------------------------
# Playfair helpers
# ---------------------------
def _make_playfair_matrix(keyword):
    # Prepare 5x5 matrix (I/J merged -> we'll skip J)
    used = []
    key_filtered = []
    for ch in keyword.upper():
        if not ch.isalpha():
            continue
        ch = ch.upper()
        if ch == 'J':
            ch = 'I'
        if ch not in used:
            used.append(ch)
            key_filtered.append(ch)
    for ch in ALPHA:
        if ch == 'J':  # skip J
            continue
        if ch not in used:
            used.append(ch)
    # build 5x5
    matrix = [used[i*5:(i+1)*5] for i in range(5)]
    pos = {}
    for r in range(5):
        for c in range(5):
            pos[matrix[r][c]] = (r, c)
    return matrix, pos

def _pairify_for_playfair(text):
    """Given a string of letters (A-Z with J replaced by I), insert X between repeated letters in a digram.
       Return (padded_text, filler_positions) where filler_positions are indices (0-based) in the padded_text
       where a filler 'X' was inserted.
    """
    i = 0
    padded = []
    filler_positions = []
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else None
        if b is None:
            padded.append(a)
            padded.append('X')
            filler_positions.append(len(padded)-1)
            i += 1
        elif a == b:
            padded.append(a)
            padded.append('X')
            filler_positions.append(len(padded)-1)
            i += 1
        else:
            padded.append(a)
            padded.append(b)
            i += 2
    return ''.join(padded), filler_positions

def playfair_encrypt(letters, keyword):
    if not letters:
        return '', []
    matrix, pos = _make_playfair_matrix(keyword)
    padded, filler_positions = _pairify_for_playfair(letters)
    cipher = []
    for i in range(0, len(padded), 2):
        a = padded[i]; b = padded[i+1]
        ra, ca = pos[a]; rb, cb = pos[b]
        if ra == rb:
            cipher.append(matrix[ra][(ca+1)%5])
            cipher.append(matrix[rb][(cb+1)%5])
        elif ca == cb:
            cipher.append(matrix[(ra+1)%5][ca])
            cipher.append(matrix[(rb+1)%5][cb])
        else:
            cipher.append(matrix[ra][cb])
            cipher.append(matrix[rb][ca])
    return ''.join(cipher), filler_positions

def playfair_decrypt(cipherletters, keyword):
    if not cipherletters:
        return ''
    matrix, pos = _make_playfair_matrix(keyword)
    # need inverse lookup for matrix by coordinates
    out = []
    for i in range(0, len(cipherletters), 2):
        a = cipherletters[i]; b = cipherletters[i+1]
        ra, ca = pos[a]; rb, cb = pos[b]
        if ra == rb:
            out.append(matrix[ra][(ca-1)%5])
            out.append(matrix[rb][(cb-1)%5])
        elif ca == cb:
            out.append(matrix[(ra-1)%5][ca])
            out.append(matrix[(rb-1)%5][cb])
        else:
            out.append(matrix[ra][cb])
            out.append(matrix[rb][ca])
    return ''.join(out)

# ---------------------------
# Pipeline: Encrypt / Decrypt note
# ---------------------------
def encrypt_note(plaintext, caesar_shift, vigenere_key, playfair_keyword):
    letters, non_alpha_positions, j_positions, original_length = _record_non_alpha_and_letters(plaintext)
    # Caesar
    after_caesar = caesar_encrypt_letters(letters, caesar_shift)
    # Vigenere
    after_vig = vigenere_encrypt_letters(after_caesar, vigenere_key)
    # Playfair (pad -> encrypt)
    padded_for_playfair, filler_positions = _pairify_for_playfair(after_vig)
    cipher_playfair, _ = playfair_encrypt(padded_for_playfair, playfair_keyword)  # playfair_encrypt also returns filler positions, but we've recorded them already
    # store metadata needed for perfect reversal
    metadata = {
        'original_length': original_length,
        'non_alpha_positions': non_alpha_positions,    # list of (idx,char)
        'j_positions': j_positions,                    # within letters (pre-padding)
        'filler_positions': filler_positions,          # indices in padded_for_playfair where 'X' was inserted
        'letters_length_before_padding': len(after_vig)
    }
    return cipher_playfair, metadata

def decrypt_note(ciphertext_letters, caesar_shift, vigenere_key, playfair_keyword, metadata):
    # 1) Playfair decrypt -> yields padded letters
    padded_letters = playfair_decrypt(ciphertext_letters, playfair_keyword)
    # 2) Remove filler characters using metadata filler_positions (remove from padded_letters)
    # Remove in descending order of indices to avoid shifting
    padded_list = list(padded_letters)
    for idx in sorted(metadata['filler_positions'], reverse=True):
        if 0 <= idx < len(padded_list):
            padded_list.pop(idx)
    after_vig = ''.join(padded_list)
    # Check length matches expected
    if len(after_vig) != metadata['letters_length_before_padding']:
        # something went wrong, but continue best-effort
        pass
    # 3) Vigenere decrypt
    after_caesar = vigenere_decrypt_letters(after_vig, vigenere_key)
    # 4) Caesar decrypt
    letters_only = caesar_decrypt_letters(after_caesar, caesar_shift)
    # At this point letters_only is the original letters with I used where J might have been.
    # Restore J's at recorded j_positions
    letters_list = list(letters_only)
    for pos in metadata.get('j_positions', []):
        if 0 <= pos < len(letters_list):
            letters_list[pos] = 'J'
    letters_only_restored = ''.join(letters_list)
    # 5) Reinsert non-alpha characters into original positions
    plaintext_reconstructed = _reinsert_non_alpha(metadata['original_length'], letters_only_restored, metadata['non_alpha_positions'], [])
    # Note: we passed empty j_positions to _reinsert_non_alpha because we already restored J's above.
    return plaintext_reconstructed
