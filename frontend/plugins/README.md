// SweetAlert2 Plugin
// 
// Este plugin configura o SweetAlert2 para uso global no aplicativo.
// 
// Uso:
// 
// 1. Toast (notificação no canto superior direito):
//    const { $toast } = useNuxtApp()
//    $toast.fire({ icon: 'success', title: 'Operação realizada!' })
// 
// 2. Alertas customizados:
//    const { $alert } = useNuxtApp()
//    await $alert.success('Sucesso!', 'Operação realizada com sucesso')
//    await $alert.error('Erro!', 'Algo deu errado')
//    await $alert.warning('Atenção!', 'Verifique os dados')
//    await $alert.info('Informação', 'Dados importantes')
// 
// 3. Confirmação:
//    const { $alert } = useNuxtApp()
//    const result = await $alert.confirm('Tem certeza?', 'Esta ação não pode ser desfeita')
//    if (result.isConfirmed) {
//      // Usuário confirmou
//    }
// 
// 4. SweetAlert2 completo (personalizado):
//    const { $swal } = useNuxtApp()
//    await $swal.fire({
//      icon: 'success',
//      title: 'Título',
//      text: 'Texto',
//      // ... outras opções
//    })
