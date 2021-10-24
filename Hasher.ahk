hash(Key) {
	if (IsObject(Key)) {
		Hash := &Key
	} 
	else 
	{
		if Key is integer
		{
			Hash := Key
		} 
		else if Key is float
		{
			Key := Key + 0.0, TruncatedKey := Key & -1
			if (Key == TruncatedKey)
			{
				Hash := TruncatedKey
			}
			else
			{
				VarSetCapacity(Hash, 8), NumPut(Key, Hash,, "Double"), Hash := NumGet(Hash,, "Int64")
			}
		}
		else
		{
			Hash := 0
			for _, Char in StrSplit(Key) 
			{
				Hash := 31 * Hash + Ord(Char)
			}
		}
	}
	return 0
}

