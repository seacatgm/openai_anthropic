# ---------------------------------------------------------------- draft_original.md (исходный документ; не редактировать)
DRAFT_ORIGINAL = r"""{{DRAFT_ORIGINAL}}"""
write_text(DRAFT_ORIGINAL + '\n', OUT / 'draft_original.md')
DRAFT_LINES = DRAFT_ORIGINAL.split('\n')
print(f'draft_original.md: {len(DRAFT_LINES)} строк, {len(DRAFT_ORIGINAL.split())} слов; L3 = «{DRAFT_LINES[2][:90]}…»')
