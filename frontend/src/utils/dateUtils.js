/**
 * Formata uma data ISO (yyyy-mm-dd) para o padrão brasileiro (dd/mm/aaaa).
 * Usa UTC ou T12:00:00 para evitar problemas de fuso horário que deslocam o dia.
 * @param {string} dateStr 
 * @returns {string}
 */
export function formatDatePTBR(dateStr) {
  if (!dateStr) return '--';
  try {
    const [year, month, day] = dateStr.split('-');
    if (!year || !month || !day) return dateStr;
    return `${day}/${month}/${year}`;
  } catch (e) {
    return dateStr;
  }
}

/**
 * Formata um objeto Date ou string para dd/mm/aaaa usando Intl.
 */
export function formatLongDatePTBR(date) {
  if (!date) return '--';
  return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
}
