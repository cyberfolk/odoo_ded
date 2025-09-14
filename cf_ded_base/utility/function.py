def sync_m2m_field(self_id, source_ids, target_model, reverse_field_name, check):
    """Sincronizza un campo Many2many in modo bidirezionale sullo stesso modello.

    Questa funzione assicura che se A è collegato a B, allora B sia collegato anche ad A
    tramite il campo `reverse_field_name`. Funziona anche per rimuovere i collegamenti
    se vengono recisi da un lato.

    Args:
        check (bool): Se False, non esegue alcuna azione
        self_id (int): L'ID del record principale (quello da cui si parte)
        source_ids (set[int]): Gli ID dei record che il record principale collega (es `creature_ids`, `npc_ids`, etc)
        target_model (recordset): L'elenco dei possibili target da sincronizzare (es tutti i mostri, NPC o creature)
        reverse_field_name (str): Il nome del campo Many2many opposto da sincronizzare
    """
    if not check:
        return

    for target in target_model:
        # Evita il confronto con sé stesso (utile nei collegamenti simmetrici es. npc_npc_ids)
        if target.id == self_id:
            continue

        # Ottiene il campo opposto dal target (es. creature_ids, npc_npc_ids, ecc.)
        reverse_field = getattr(target, reverse_field_name)

        # Se il record principale è collegato al target MA il target NON è collegato a lui → rimuovi
        if self_id in reverse_field.ids and target.id not in source_ids:
            setattr(target, reverse_field_name, [(3, self_id)])

        # Se il record principale è collegato al target MA il target NON è ancora collegato a lui → aggiungi
        elif self_id not in reverse_field.ids and target.id in source_ids:
            setattr(target, reverse_field_name, [(4, self_id)])
