import { useRouter } from 'next/navigation'
import { MouseEventHandler } from 'react'
import { BsPlusSquare } from 'react-icons/bs'

export const NewChatButton = (): JSX.Element => {
  const router = useRouter()

  const handleButtonClick: MouseEventHandler<HTMLButtonElement> = (e) => {
    e.preventDefault()
    console.log(window.location.href);
    if (window.location.href.endsWith('/chat')) {
      window.location.reload()
    } else {
      void router.push('/chat')
    }
  }
  
  return (
    <button
      data-testid="new-chat-button"
      className="px-4 py-2 mx-4 my-1 border border-primary bg-white dark:bg-black hover:text-white hover:bg-primary shadow-lg rounded-lg flex items-center justify-center top-1 z-20"
      onClick={handleButtonClick}
    >
      <BsPlusSquare className="h-6 w-6 mr-2" /> New Chat
    </button>
  )
}