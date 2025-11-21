import Swal from 'sweetalert2'

export default defineNuxtPlugin(() => {
  return {
    provide: {
      swal: Swal,
      toast: Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.addEventListener('mouseenter', Swal.stopTimer)
          toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
      }),
      alert: {
        success: (title: string, text?: string) => {
          return Swal.fire({
            icon: 'success',
            title,
            text,
            confirmButtonColor: '#10b981'
          })
        },
        error: (title: string, text?: string) => {
          return Swal.fire({
            icon: 'error',
            title,
            text,
            confirmButtonColor: '#ef4444'
          })
        },
        warning: (title: string, text?: string) => {
          return Swal.fire({
            icon: 'warning',
            title,
            text,
            confirmButtonColor: '#f59e0b'
          })
        },
        info: (title: string, text?: string) => {
          return Swal.fire({
            icon: 'info',
            title,
            text,
            confirmButtonColor: '#3b82f6'
          })
        },
        confirm: (title: string, text?: string) => {
          return Swal.fire({
            icon: 'question',
            title,
            text,
            showCancelButton: true,
            confirmButtonColor: '#10b981',
            cancelButtonColor: '#ef4444',
            confirmButtonText: 'Sim',
            cancelButtonText: 'Cancelar'
          })
        }
      }
    }
  }
})
