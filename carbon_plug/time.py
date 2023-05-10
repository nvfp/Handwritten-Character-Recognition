

def get_dur(__secs: float, /) -> str:
    
    hours, _r = divmod(__secs, 3600)
    minutes, seconds = divmod(_r, 60)

    hours = int(hours)
    minutes = int(minutes)
    seconds = round(seconds)

    parts = []
    
    if hours > 0:
        if hours == 1:
            parts.append('1 hr')
        else:
            parts.append(f'{hours} hrs')
    
    if minutes > 0:
        if minutes == 1:
            parts.append('1 min')
        else:
            parts.append(f'{minutes} mins')

    if seconds == 0:
        if parts == []:
            parts.append('0 sec')
    elif seconds == 1:
        parts.append('1 sec')
    else:
        parts.append(f'{seconds} secs')

    return ' '.join(parts)